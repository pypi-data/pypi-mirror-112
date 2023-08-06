import sys
import os
import json
from json import loads, dumps
import time
import datetime
import logging

import pandas as pd
import requests
import psycopg2
from jinja2 import Template


FILEPATH = os.path.join(os.path.dirname(__file__))
DATE = datetime.datetime.today().strftime('%Y%m%d')
logging.basicConfig(format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


# general functions for data manipulation

def chunks(l, n):
    #Yield successive n-sized chunks from l.
    for i in range(0, len(l), n):
        yield l[i:i + n]


def remove_namespace(string):
  # remove namespaces from string
  if isinstance(string, str) and string.startswith('http'):
      string = string.split('/')[-1]
  return string


def df2file(outfolder, outfilename, df, separator='\t'):
    """
    prints a dataframe to a tab seperated text file in folder of choice.
    """
    logger.info("printing dataframe to file: {}".format(outfilename))
    out_path = outfolder + "/" + outfilename
    out_file = open(out_path, 'w')
    df.to_csv(out_file, sep = separator, encoding = 'utf-8', index=False)
    out_file.close()


def df_from_file(file_path, sep='\t', header=0):
    """
    reads a file into a pandas dataframe
    """
    try:
        annot_file = open(file_path, 'r')
        logger.info('reading in {}'.format(file_path))
        df = pd.read_csv(annot_file, sep=sep, header=header)
        logger.info('column headers: {}'.format(df.columns))
        annot_file.close()
    except:
        logger.info('no file found: {}'.format(file_path))
        sys.exit(1)
    return df


def dflist_from_folder(file_list, folder_path):
    """
    reads a designated list of files from a designated folder into a list of dataframes
    """
    dflist=[]
    for each in file_list:
      try:
        annot_file_path = folder_path+"/"+each
        annot_file = open(annot_file_path, 'r')
        logger.info('reading in {}'.format(each))
        annot_df = pd.read_csv(annot_file, sep='\t', dtype='object')
        dflist.append(annot_df)
      except:
        logger.info('no file named: {}'.format(each))
        continue
    return dflist


def collapse_columns(df, groupby, col_list, separator=';'):
    """
    collapses values in column list into lists grouped by groupby and separated with ';'
    and returns the reformatted dataframe
    """
    for each in col_list:
        if each == groupby:
            continue
        else:
            print('collapsing column: ' + each)
            df_e = df.dropna(subset=[each])
            df_e[each]= df_e[each].astype(str)
            df_e = df_e.groupby(groupby)[each].agg(lambda x: separator.join(pd.unique(x))).reset_index()
            df = df.drop([each], axis=1)
            df = pd.merge(df, df_e, left_on=groupby, right_on=groupby, how = 'outer')
    return df


def prefix_column_names(prefix, dataframe, skip=[""]):
    """
    add a prefix to the column names of a datframe, skipping any as required.
    """
    for each in dataframe.columns:
        if each in skip:
          continue
        else:
          new = prefix + each
          dataframe = dataframe.rename(columns={each:new})
    return dataframe


# functions for querying the marrs graphql api

def run_ceres_query(query, config, query_name, input_list, limit=500, offset=0, chunk_size=100, debug=False, taxon=None, List=True):
    """
    Runs a list of identifier inputs through a query against the ceres api.  The chunk_size determines how many identifiers are run
    in a single query.  Use chunk_size=1 and List=False to run a query formatted for a single id.  The result data are then flattened
    into a dataframe.  The query_name is used solely for logging progress.
    """
    input_set = set()
    for x in input_list:
      input_set.add(x)
    input_list = list(input_set)
    logger.info('running {}'.format(query_name))
    logger.info('{} unique elements in the input list'.format(len(input_list)))
    logger.info('Limit: {0}, Offset: {1}'.format(limit, offset))
    graphql_query = query
    all_results = []
    chunked_input_list = chunks(sorted(input_list), chunk_size)
    chunk_count = 0
    logger.debug("{} query: {}".format(query_name,graphql_query))
    for l in chunked_input_list:
        chunk_count += len(l)
        logger.info('Running {2} query {0}/{1}'.format(chunk_count, len(input_list),query_name))
        logger.debug('{}'.format(','.join(l)))
        if List == False:
            l=l[0]
        graphql_variables = {
          "input": l,
          "limit": int(limit),
          "offset": int(offset)
            }
        if taxon:
            graphql_variables.update({'taxon': taxon})
        # submit the graphql query with all input variables
        result = run_graphql_query(graphql_query, graphql_variables, config) # run the request
        #print(result.text)
        json_data = json.loads(result.text) #load the returned data
        check_graphql_json(json_data, limit)
        # get a flattened list of results from the nested json
        result_list = flatten_json(json_data['data'])
        if debug == True:
          logger.info(result_list)
        if result_list:
            result_df = pd.DataFrame(result_list)
            all_results.append(result_df)
    result_df = pd.concat(all_results)
    result_df = result_df.drop_duplicates()
    print(result_df.head())
    return result_df


def check_graphql_config(config_file):
    """
    Submits a simple graphql request to validate that the graphql server
    is up and running and that the configuration is valid.
    """
    logger.info('Checking that Graphql configuration is valid')
    with open(config_file) as json_file:
        config = json.load(json_file)
    headers = {
        'authorization': 'Bearer {}'.format(config['token'])
    }
    authentication_url = config['graphql'].replace('/graphql', '/auth/me')
    try:
        response = requests.get(authentication_url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as error:
        logger.error(
            'Unable to validate config. Receiving {} error'.format(
                response.status_code)
        )
        logger.debug(error)
        sys.exit(1)
    return


def get_graphql_template(query):
    """
    Returns a string object containing the templated graphql query.
    Using the input list of identifiers a graphql template is filled in.
    """
    file_path = os.path.dirname(os.path.abspath(query))
    file_name = os.path.basename(query)
    with open('{0}/{1}'.format(file_path, file_name), 'r') as f:
        query_template = f.read()
    return query_template


def run_graphql_query(query, variables, config):
    """
    runs a formatted query with variables against a graphql endpoint specified in the config file.
    The function makes 3 attempts at running the query before terminating.
    """
    headers = {
        'authorization': 'Bearer {}'.format(config['token'])
    }
    try:
        response = requests.post(config['graphql'], json={'query': query, 'variables': variables}, headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as error:
        logger.error(
            'Unable to submit Graphql request. Receiving {} error'.format(
                response.status_code)
        )
        logger.debug(error)
        logger.warning(query)
        logger.warning(variables)
        logger.info("pausing script for 1 minute")
        time.sleep(60)
        try:
            logger.info ("running second attempt")
            response = requests.post(config['graphql'], json={'query': query, 'variables': variables}, headers=headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            logger.error(
                'Unable to submit Graphql request. Receiving {} error'.format(
                    response.status_code)
            )
            logger.debug(error)
            logger.warning(query)
            logger.warning(variables)
            time.sleep(60)
            try:
                logger.info ("running third and final attempt")
                response = requests.post(config['graphql'], json={'query': query, 'variables': variables}, headers=headers)
                response.raise_for_status()
            except requests.exceptions.HTTPError as error:
                logger.error(
                    'Unable to submit Graphql request. Receiving {} error'.format(
                        response.status_code)
                )
                logger.debug(error)
                logger.warning(query)
                logger.warning(variables)
                sys.exit(1)
    return response


def flatten_json(data, parent_result_list=None, parent_key=None):
    """
    Returns a list of dictionaries. This function will recursively
    search through a nested dictionary object flattening out the results
    so that they can be converted into a pandas dataframe.
    """
    if not isinstance(data, dict):
        raise Exception('Incorrect input data type {}. Expected dict.'.format(type(data)))
    if not parent_result_list:
        parent_result_list = [{}]
    for key, value in data.items():
        if not isinstance(value, (dict, list)):
            new_result_list = []
            for result in parent_result_list:
                if parent_key:
                    new_key = '{}.{}'.format(parent_key, key)
                    str_result = {new_key:value}
                else:
                    str_result = {key:value}
                output_result = {**result, **str_result}
                new_result_list.append(output_result)
            parent_result_list = new_result_list
    for key, value in data.items():
        if parent_key:
            new_key = '{}.{}'.format(parent_key, key)
        else:
            new_key = key
        if isinstance(value, list):
            if not value:
                continue
            new_result_list = []
            for item in value:
                new_parent_result = flatten_json(item, parent_result_list, new_key)
                new_result_list.extend(new_parent_result)
            parent_result_list = new_result_list
        if isinstance(value, dict):
            new_result_list = flatten_json(value, parent_result_list, new_key)
            parent_result_list = new_result_list
    if not parent_result_list:
        logger.warning('No data in json response')
    return parent_result_list


def recursive_key_count(data):
    """
    Yields the length of all lists in a nested dictionary
    type structure. Used for checking that the length
    of lists does not exceed the predefined limit.
    """
    for key, value in data.items():
        if isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    yield from recursive_key_count(item)
            yield (key, len(value))
        elif isinstance(value, dict):
            yield from recursive_key_count(value)


def check_graphql_json(json_data, limit):
    counter=0
    error_fields = set()
    for result in recursive_key_count(json_data):
        if int(result[1]) == int(limit):
            counter+=1
            error_fields.add(result[0])
    if counter > 1:
        error_fields_string = ', '.join(error_fields)
        warning_message = '{} fields including {} have the same number of \
        results as the query limit of {}. This may result in missing data. You may \
        want to consider increasing the upper limit to a higher value'.format(
    counter, error_fields_string, limit
    )
        logger.warning(warning_message)
    else:
        logger.debug('No fields in the returned JSON data exceed the upper limit')


def psql_query(query, config):
    """
    connect and query MARRS PSQL
    """
    with psycopg2.connect(dbname=config['psql']['dbname'],
                          user=config['psql']['user'],
                          password=config['psql']['password'],
                          host=config['psql']['host'],
                          port=config['psql']['port']) as connection:
        with connection.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()


# common MARRS extraction functions

def getNamespace(gene,sparql):
    # return the MARRS namespace for an ensembl gene identifier
    # nb this is only going to work when the ensembl identifier is in a MARRS graph
    GENE = gene
    mylist = []
    q = """
    SELECT DISTINCT ?gene
    WHERE
    {
    VALUES ?gene {<http://identifiers.org/ensembl.fungi/"""+GENE+"""> <http://identifiers.org/ensembl/"""+GENE+"""> <http://identifiers.org/ensembl.plant/"""+GENE+"""> <http://identifiers.org/ensembl.metazoa/"""+GENE+""">  <http://identifiers.org/ensembl.protist/"""+GENE+""">}
    {
    GRAPH ?g
    {?gene ?p ?s .}}
    UNION
    {
    GRAPH ?g
    { ?s ?p ?gene .}}
    }
    LIMIT 2
    """
    sparql.setQuery(q)
    results = sparql.query().convert()
    namespace = "http://identifiers.org/ensembl"
    ns_length1 = len(namespace)
    for binding in results["results"]["bindings"]:
        fullgene = binding["gene"]["value"]
        namespace2 = fullgene.rsplit('/',1)[0]
        ns_length2 = len(namespace2)
        if ns_length2 > ns_length1:
            namespace = namespace2
    return namespace


def getTaxon(geneurl, sparql):
    # return the scientific name for a complete gene identifier url
    GENE = geneurl
    print ("\tgetting taxon for; " + geneurl)
    mylist = []
    q = """
    SELECT DISTINCT ?t ?sp ?sn
    WHERE {
    GRAPH ?graph {
        ?prot ?p <""" + GENE + """> .
        ?prot <http://purl.uniprot.org/core/organism> ?t .
      }
    GRAPH <http://marrs.generalbioinformatics.com/ontology/taxon> {
        ?t <http://generalbioinformatics.com/ontologies/taxonomy#hasParent>* ?sp .
        ?sp a <http://generalbioinformatics.com/ontologies/taxonomy#Species> .
        ?sp <http://generalbioinformatics.com/ontologies/taxonomy#scientificName> ?sn .
      }
    }
    """
    sparql.setQuery(q)
    results = sparql.query().convert()
    sciName = ""
    for binding in results["results"]["bindings"]:
        sciName = binding["sn"]["value"]
        taxID = binding["sp"]["value"]
    return sciName


def peptideExtraction(ncbi_taxon, sparql):
    """extracts all ensembl peptides for a taxon that are found in ensembl"""
    logger.info('Extracting all ensembl peptides for {}'.format(ncbi_taxon))
    output = set()
    q = """
    PREFIX csim-voc: <http://generalbioinformatics.com/ontologies/crossSystemIdMapping#>
    SELECT DISTINCT ?peptide ?gene
    WHERE {
    GRAPH <http://marrs.generalbioinformatics.com/crossSystemIdmapping/ensembl> {
        ?gene csim-voc:x-taxonomy <http://identifiers.org/taxonomy/"""+str(ncbi_taxon)+"""> .
        ?gene csim-voc:hasTranscript ?csim_transcript .
        ?csim_transcript csim-voc:hasPeptide ?peptide .
    }
    }
    """
    sparql.setQuery(q)
    results = sparql.query().convert()
    for binding in results["results"]["bindings"]:
        peptide = binding["peptide"]["value"]
        gene = binding["gene"]["value"]
        output.add((peptide, gene))
    return output


def geneExtraction(taxon, sparql):
    """extracts all ensembl genes and peptides for a CPSD taxon that are found in ensembl"""
    mylist = []
    q = """
    PREFIX csim: <http://generalbioinformatics.com/data/crossSystemIdMapping#>
    PREFIX csimo: <http://generalbioinformatics.com/ontologies/crossSystemIdMapping#>
    SELECT DISTINCT ?gene
    WHERE {
    GRAPH <http://marrs.generalbioinformatics.com/crossSystemIdmapping/ensembl> {
        ?gene a csim:EnsemblGene .
        ?gene csimo:hasTranscript ?transcript .
        ?transcript csimo:hasPeptide ?ensembl_peptide .
        ?cpsd_peptide csimo:hasPeptide ?ensembl_peptide .
        }
    GRAPH <http://marrs.generalbioinformatics.com/crossSystemIdmapping/cpsd> {
        ?ag csimo:hasPeptide ?cpsd_peptide .
        ?vo csimo:hasAssemblyGroup ?ag .
        ?vo csimo:hasOrganism ?org .
        ?org csimo:x-taxonomy <http://identifiers.org/taxonomy/"""+str(taxon)+""">  .
    }
    }
    """
    sparql.setQuery(q)
    results = sparql.query().convert()
    for binding in results["results"]["bindings"]:
        gene = binding["gene"]["value"]
        mylist.append(gene)
    return mylist


def enzymeExtraction(sparql):
    "extracts all enzyme identifiers from MARRS"
    myset=set()
    q="""
        SELECT DISTINCT ?enzyme
        WHERE {
        GRAPH <http://marrs.generalbioinformatics.com/Uniprot>
        {
            ?enzyme a <http://purl.uniprot.org/core/Enzyme>
        }
        }
    """
    sparql.setQuery(q)
    results = sparql.query().convert()
    for binding in results["results"]["bindings"]:
        enzyme = binding["enzyme"]["value"]
        enzyme = remove_namespace(enzyme)
        if "-" in enzyme:
            continue
        else:
            myset.add(enzyme)
    logger.info("extracted {} distinct enzyme identifiers".format(str(len(myset))))
    mylist = list(myset)
    mydf = pd.DataFrame(mylist, columns=["enzyme"])
    return mydf


# functions required for the project ETLs


def getOrths(input_list, target_taxon_list, config, limit = 1000, offset = 0, chunk_size=100):
    # retreive homologs from ceres
    # TODO: update to get nicer ids/accessions
    if len(input_list) >30:
        longlist=True
    chunked_input_list = chunks(sorted(input_list), chunk_size)
    chunk_count = 0
    taxon_list = target_taxon_list
    logger.info('{} elements in the taxon list'.format(len(taxon_list)))
    logger.info('{} elements in the input list'.format(len(input_list)))
    # logger.info('{}'.format(','.join(input_list)))
    logger.info('Limit: {0}, Offset: {1}'.format(limit, offset))
    all_results = []
    graphql_query = """
        query gene2homologs($input: [String], $taxon: [String]!, $limit: Int!, $offset: Int!){
          genes(ids: $input){
            ensembl_gene_id
            peptides(limit: $limit, offset: $offset){
              homologs(taxonIds:$taxon){
                peptide{
                  genes{
                    ensembl_gene_id
                  }
                  ensembl_peptide_id
                  organism{
                    id
                  }
                }
              }
            }
          }
          }
        """
    logger.debug("homolog graphql query: {}".format(graphql_query))
    for l in chunked_input_list:
        chunk_count += len(l)
        logger.info('Retrieving homologs {0}/{1}'.format(
            chunk_count, len(input_list)))
        logger.debug('{}'.format(','.join(l)))
        graphql_variables = {
          "input": l,
          "taxon": taxon_list,
          "limit": int(limit),
          "offset": int(offset)
            }

        # submit the graphql query with all input variables
        result = run_graphql_query(graphql_query, graphql_variables, config)
        json_data = json.loads(result.text) #load the returned data
        check_graphql_json(json_data, limit)
        # get a flattened list of results from the nested json
        result_list = flatten_json(json_data['data'])
        if result_list:
            result_df = pd.DataFrame(result_list)
            # print(result_df)
            # print(result_df.columns)
            all_results.append(result_df)
    result_df = pd.concat(all_results)
    # print(result_df.columns)
    result_df = result_df[["genes.ensembl_gene_id",
    "genes.peptides.homologs.peptide.ensembl_peptide_id",
    "genes.peptides.homologs.peptide.genes.ensembl_gene_id",
    "genes.peptides.homologs.peptide.organism.id"]]
    cols = ["input_gene", "ortholog_peptide", "ortholog_gene",
                            "ortholog_taxon"]
    result_df.columns = cols
    result_df.input_gene = result_df.input_gene.apply(remove_namespace)
    result_df.ortholog_peptide = result_df.ortholog_peptide.apply(remove_namespace)
    result_df.ortholog_gene = result_df.ortholog_gene.apply(remove_namespace)
    result_df.ortholog_taxon = result_df.ortholog_taxon.apply(remove_namespace)
    result_df = result_df.dropna().drop_duplicates() # remove strange and duplicated results
    return result_df


def pchemblactive(input_list, config, limit = 500, offset = 0, chunk_size=100):
    """returns genes with an entry in ChEMBL
    with a pChembl >= 6 """
    logger.info("running pchemblactive")
    logger.info('{} elements in the input list'.format(len(input_list)))
    logger.info('Limit: {0}, Offset: {1}'.format(limit, offset))
    chunked_input_list = chunks(sorted(input_list), chunk_size)
    chunk_count = 0
    all_results = []
    graphql_query = """
    query gene2pchembl($input: [String], $limit: Int!, $offset: Int!){
    genes(ids: $input, limit: $limit, offset: $offset) {
        accession_id
        proteins(chemblmap: true) {
            chembltargets {
                max_pchembl
                }
            }
        }
    }
    """
    gene_count=0
    logger.debug("pchembl active graphql query: {}".format(graphql_query))
    for l in chunked_input_list:
        chunk_count += len(l)
        logger.info('Running pchemblactive query {0}/{1}'.format(
            chunk_count, len(input_list)))
        logger.debug('{}'.format(','.join(l)))
        gene_count += 1
        graphql_variables = {
          "input": l,
          "limit": int(limit),
          "offset": int(offset)
            }
        # submit the graphql query with all input variables
        result = run_graphql_query(graphql_query, graphql_variables, config) # run the request
        #print (result.text)
        json_data = json.loads(result.text) #load the returned data
        check_graphql_json(json_data, limit)
        # get a flattened list of results from the nested json
        result_list = flatten_json(json_data['data'])
        if result_list:
            result_df = pd.DataFrame(result_list)
            all_results.append(result_df)
    result_df = pd.concat(all_results)
    result_df = result_df[["genes.accession_id",
                "genes.proteins.chembltargets.max_pchembl"]]
    result_df = result_df.dropna().drop_duplicates()
    cols = ["gene", "pchembl"]
    result_df.columns = cols
    result_df = result_df.loc[result_df.groupby(['gene'])['pchembl'].idxmax()]
    #print(result_df.columns)
    result_df = result_df.loc[result_df['pchembl']>=6]
    result_df = result_df[['gene','pchembl']]
    result_df=result_df.drop_duplicates()
    #print (result_df.shape)
    #print(result_df.columns)
    print(result_df.head())
    return result_df


def biomartwget(query, taxon, categorisation, namespace):
    """
    Convert a list of ids from a biomart query into a set of data for lead generation
    """
    logger.info('Submitting http request to url:')
    logger.info(query)
    try:
        response = requests.get(query)
        response.raise_for_status()
    except requests.exceptions.HTTPError as error:
        logger.warning('Unable to submit request. Receiving {} error'.format(
            response.status_code))
    biomart_list = response.text.splitlines()
    output = set()
    for biomart_identifier in biomart_list:
        output.add(biomart_identifier.strip() + '\t' + categorisation + '\t' +
                   taxon + '\t' + namespace + '\n')
    return output


def dartable_genome_check(gene_list, sparql):
    with open('{}/templates/dartable_genome_check.sparql.j2'.format(FILEPATH),
              'r') as jinja:
        template_sparql_jinja = Template(jinja.read())
    chunk_count = 0
    dartable_genes = set()
    logger.info('Dartable genome check')
    logger.info('Checking {} genes'.format(len(gene_list)))
    template_sparql_query = template_sparql_jinja.render()
    sparql.setQuery(template_sparql_query)
    results = sparql.query().convert()
    for binding in results["results"]["bindings"]:
        dartable_genes.add(binding['gene']["value"])

    dartable_genes = set([str(i.rsplit('/', 1)[1]) for i in dartable_genes])

    overlapping_genes = set(gene_list).intersection(dartable_genes)
    logger.info('{} overlapping dartable genes'.format(len(overlapping_genes)))
    return overlapping_genes


def dartGen(HsEns, sparql):
    out = False
    q = """
    SELECT DISTINCT ?s
    WHERE {
    GRAPH <http://marrs.generalbioinformatics.com/project/List> {
     ?s <http://www.w3.org/2000/01/rdf-schema#label> "DARTABLE GENOME" .
     ?s <http://generalbioinformatics.com/ontologies/project#hasMember> <http://identifiers.org/ensembl/""" + HsEns + """> .
        }
    }
    """
    sparql.setQuery(q)
    results = sparql.query().convert()
    for binding in results["results"]["bindings"]:
        if "s" in binding:
            out = True
    return out


def golistDm(golistName, sparql, taxon):
    # return list of Dm genes annotated with GO from named list of GOs
    mylist = []
    LIST = '"' + golistName + '"'
    q = """
        SELECT DISTINCT ?gene (GROUP_CONCAT(DISTINCT ?go ; separator=";") as ?go)
        WHERE {
        GRAPH <http://marrs.generalbioinformatics.com/project/List> {
         ?s <http://www.w3.org/2000/01/rdf-schema#label> """ + LIST + """ .
         ?s <http://generalbioinformatics.com/ontologies/project#hasMember> ?go .
        }
        GRAPH <http://marrs.generalbioinformatics.com/Uniprot> {
         ?uniprot ?xref ?go .
         ?uniprot <http://purl.uniprot.org/core/organism> <http://identifiers.org/taxonomy/""" + str(
        taxon) + """> .
         ?uniprot <http://generalbioinformatics.com/ontologies/uniprot#x-ensembl-gene> ?gene .
        }
        }
        """
    sparql.setQuery(q)
    results = sparql.query().convert()
    for binding in results["results"]["bindings"]:
        dmgene = binding["gene"]["value"]
        GO = binding["go"]["value"]
        out = [dmgene, GO]
        mylist.append(out)
    return mylist


def pdbDirect(geneList, sparql):
    # return direct hit from pdb
    geneList = list(set(geneList))
    mylist = []
    mylist1 = set()
    mylist2 = []

    gene_list_chunks = chunks(geneList, 750)
    with open('{}/templates/ensembl_pdb_direct.sparql.j2'.format(FILEPATH),
              'r') as jinja:
        template_sparql_jinja = Template(jinja.read())
    chunk_count = 0
    for gene_list_chunk in gene_list_chunks:
        chunk_count += len(gene_list_chunk)
        logger.info('{0}/{1}'.format(chunk_count, len(geneList)))
        template_sparql_query = template_sparql_jinja.render(
            gene_list=gene_list_chunk)
        PDB = ""
        sparql.setQuery(template_sparql_query)
        results = sparql.query().convert()
        for binding in results["results"]["bindings"]:
            PDB = binding["pdb"]["value"]
            sciName = binding["sciName"]["value"]
            taxonId = binding["taxon"]["value"]
            ENSEMBL = binding["gene"]["value"]
            out = [ENSEMBL, PDB, taxonId]
            out2 = [ENSEMBL.split('/')[-1], sciName]
            mylist.append(out)
            mylist1.add(sciName)
            mylist2.append(out2)
    df = pd.DataFrame(mylist2, columns=["ortholog_gene", "species"])
    return mylist, mylist1, df


def annotatePDB(graph, protein_dict, minId, minCov, sparql, namespace):
    # return chembl or pdb hit from relate
    #print "running annotate CHEMBL function: " + gene + ": " + destGraph
    RG = graph
    mylist = []
    hits = set()

    with open('{}/templates/pdb_annotate.sparql.j2'.format(FILEPATH),
              'r') as jinja:
        template_sparql_jinja = Template(jinja.read())

    hits = {}
    chunk_count = 0
    protein_count = len(protein_dict.keys())
    for protein_chunk in chunks(list(protein_dict.keys()), 4000):
        chunk_count += len(protein_chunk)
        logger.info("PDB annotation: {0}/{1}".format(chunk_count,
                                                     protein_count))
        template_sparql_query = template_sparql_jinja.render(
            graph=graph, uris=protein_chunk)
        print(template_sparql_query)
        sparql.setQuery(template_sparql_query)
        results = sparql.query().convert()
        for binding in results["results"]["bindings"]:
            hit_count = binding["hit_count"]["value"]
            protein = binding["protUri"]["value"]
            hits[protein] = hit_count

    for key, value in hits.items():
        gene_uri = protein_dict[key]
        prior = str(value) + " blast hits in PDB with minimum " + str(
            minId) + "% identity and " + str(minCov) + "% coverage"

        gene_id = gene_uri.rsplit('/', 1)[1]
        out = [gene_id, prior]
        mylist.append(out)

    logger.info('PDB annotation contains {} entries'.format(len(mylist)))
    return mylist


# Not in use

def getOrths_ensembl(genes, taxons, config):
    #return Ensembl orthologs from MARRS PSQL
    if len(genes) > 1:
        g = tuple(genes)
    else:
        g = (genes[0], 'wibble')
    if len(taxons) > 1:
        t = tuple(taxons)
    else:
        t = (taxons[0], '1234')
    rows = psql_query(
        """
    SELECT id, left_percent_identity, left_percent_coverage, left_ensembl_gene_id, left_ensembl_protein_id, right_ensembl_gene_id, right_ensembl_protein_id, right_cpsd_taxon, left_cpsd_taxon, match_type, compara
    FROM ensembl_homologies AS Homologs
    WHERE Homologs.left_ensembl_gene_id IN {gene_identifiers!r}
    AND Homologs.left_cpsd_taxon != Homologs.right_cpsd_taxon
    AND Homologs.right_cpsd_taxon IN {taxon_ids!r}
    ORDER BY Homologs.left_ensembl_gene_id ASC;
    """.format(gene_identifiers=g, taxon_ids=t), config)
    myArray = []
    for row in rows:
        out = [row[3], row[5], row[6], row[7]]
        myArray.append(out)
    mydf = pd.DataFrame(myArray,
                        columns=[
                            "input_gene", "ortholog_gene", "ortholog_peptide",
                            "ortholog_taxon"
                        ])
    #print mydf
    return mydf


def ensemblCheckFailure(gene, server):
    # This drosophila Id has not been found in Ensembl. Test why

    # getting issue where the ensembldb has updated ids and the lookup is failing due to that.
    # check ensembl api is live
    response = "false"
    extPing = "/info/ping?"
    rPing = requests.get(server + extPing,
                         headers={"Content-Type": "application/json"})
    if not rPing.ok:
        print ("Ensembl API service is down. Ping failed")
        rPing.raise_for_status()
        sys.exit()
    else:
        # can check that the id is present
        ext = "/lookup/id"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        searchIds = '{ "ids" : ["' + gene + '"]}'
        rExists = requests.post(server + ext, headers=headers, data=searchIds)
        if not rExists.ok:
            print ("Failed in checking ensembl id lookup: " + gene)
            rExists.raise_for_status()
            sys.exit()

        decoded = rExists.json()
        #print decoded[gene]
        if str(decoded[gene]) == "None":
            print ("This ID is not in the current Ensembl release: " + gene)
            response = "true"
        else:
            print ("This ID is in the current Ensembl release, but failed the ortholog lookup. Investigate: " + gene + " . We will try using the id-mapping graph.")
            sys.exit()
        # end if
    # end if
    return response
