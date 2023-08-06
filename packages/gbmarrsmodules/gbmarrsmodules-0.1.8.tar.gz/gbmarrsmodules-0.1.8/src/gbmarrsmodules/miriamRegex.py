import re

# regular expressions from https://www.ebi.ac.uk/miriam/main/collections
# When adding new patterns to this file, indicate if modifications have been made to the miriam standard, eg changing case

miriamPattern = {}
#A
#B
miriamPattern["bindingDB"] = "^\d+$"
#C
miriamPattern["cas"] = "^\d{1,7}\-\d{2}\-\d$"
miriamPattern["cgd"] = "^CAL\d{7}$"
miriamPattern["chebi"] = "^CHEBI:\d+$"
miriamPattern["chembl.compound"] = "^CHEMBL\d+$"
miriamPattern["chembl.target"] = "^CHEMBL\d+$"
miriamPattern["cl"] = "^CL:\d{7}$"
miriamPattern["clinvar.record"] = "^RCV\d+(\.\d+)?$"
miriamPattern["clinvar.submission"] = "^SCV\d+(\.\d+)?$"

#D
miriamPattern["dbsnp"] = "^rs\d+$"
#E
miriamPattern["ec-code"] = "^\d+\.-\.-\.-|\d+\.\d+\.-\.-|\d+\.\d+\.\d+\.-|\d+\.\d+\.\d+\.(n)?\d+$"
miriamPattern["efo"] = "^\d{7}$"
miriamPattern["ensembl"] = "^((ENS[A-Z]*[FPTG]\d{11}(\.\d+)?)|(FB\w{2}\d{7})|(Y[A-Z]{2}\d{3}[a-zA-Z](\-[A-Z])?)|([A-Z_a-z0-9]+(\.)?(t)?(\d+)?([a-z])?))$"
miriamPattern["ensembl.bacteria"] = "^((EB\w+)|([A-Z0-9]+\_[A-Z0-9]+))$"
miriamPattern["ensembl.fungi"] = "^[A-Z-a-z0-9]+$"
miriamPattern["ensembl.metazoa"] = "^\w+(\.)?\d+$"
miriamPattern["ensembl.plant"] = "	^\w+(\.\d+)?(\.\d+)?$"
miriamPattern["ensembl.protist"] = "^\w+$"
#F
miriamPattern["flybase"] = "^FB\w{2}\d{7}$"
#G
miriamPattern["go"] = "^GO:\d{7}$"
#H
# miriamPattern["hapmap"] Has no Miriam entry
miriamPattern["hgnc"] = "^((HGNC|hgnc):)?\d{1,5}$" # Need to change from ^((HGNC|hgnc):)?\d{1,5}$ to remove case discrepancy
miriamPattern["hgnc.family"] = "^[A-Z0-9-]+(#[A-Z0-9-]+)?$"
miriamPattern["hgnc.genefamily"] = "^\d+$"
miriamPattern["hgnc.symbol"] = "^[A-Za-z-0-9_]+(\@)?$"
miriamPattern["hp"] = "^HP:\d{7}$"
#I
miriamPattern["inchi"] = "^InChI\=1S?\/[A-Za-z0-9\.]+(\+[0-9]+)?(\/[cnpqbtmsih][A-Za-z0-9\-\+\(\)\,\/\?\;\.]+)*$"
miriamPattern["inchikey"] = "^[A-Z]{14}\-[A-Z]{10}(\-[A-Z])?"
miriamPattern["intact"] = "^EBI\-[0-9]+$"
miriamPattern["interpro"] = "^IPR\d{6}$"
#J
#K
#L
#M
miriamPattern["mp"] = "^MP:\d{7}$"
miriamPattern["medgen"] = "^[CN]*\d{4,7}$"
miriamPattern["mesh"] = "^(C|D)\d{6}$"
miriamPattern["mgi"] = "^MGI:\d+$"
#N
miriamPattern["nbcigene"] = "^\d+$"
#O
miriamPattern["omim"] = "^[*#+%^]?\d{6}$"
miriamPattern["orphanet"] = "^\d+$"
miriamPattern["orthodb"] = "^\w+$"
#P
miriamPattern["pdb"] = "^[0-9][A-Z0-9]{3}$" # changed from ^[0-9][A-Za-z0-9]{3}$, must be caps for integration
miriamPattern["pfam"] = "^PF\d{5}$"
miriamPattern["pubchem.compound"] = "^\d+$"
miriamPattern["pubchem.substance"] = "^\d+$"
miriamPattern["pubmed"] = "^\d+$"
#Q
#R
miriamPattern["reactome"] = "(^R-[A-Z]{3}-\d+(-\d+)?(\.\d+)?$)|(^REACT_\d+(\.\d+)?$)"
miriamPattern["refseq"] = "^((AC|AP|NC|NG|NM|NP|NR|NT|NW|XM|XP|XR|YP|ZP)_\d+|(NZ\_[A-Z]{4}\d+))(\.\d+)?$"
#S
miriamPattern["stitch"] = "^\w{14}$"
#T
miriamPattern["taxonomy"] = "^\d+$"
#U
miriamPattern["uberon"] = "^UBERON\:\d+$"
miriamPattern["uniprot"] = "^([A-N,R-Z][0-9]([A-Z][A-Z, 0-9][A-Z, 0-9][0-9]){1,2})|([O,P,Q][0-9][A-Z, 0-9][A-Z, 0-9][A-Z, 0-9][0-9])(\.\d+)?$"
#V
#W
miriamPattern["wikipathways"] = "WP\d{1,5}(\_r\d+)?$"
#X
#Y
#Z

