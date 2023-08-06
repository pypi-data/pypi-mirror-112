import re
import os

from rdflib import Namespace

from .util import getDataRoot 


def getDownDir(dataset, dataBuild):
    dataroot = getDataRoot("data", dataBuild) # this is the location where the data should be stored from the downloaded input and output of the ETLs
    downloaddir = os.path.join (dataroot, dataset, "download/")
    return downloaddir

def getRDFDir(dataset, dataBuild):
    dataroot = getDataRoot("data", dataBuild)
    rdfdir = os.path.join (dataroot, dataset, "rdf/")
    return rdfdir

def getSQLDir(dataset, dataBuild):
    dataroot = getDataRoot("data", dataBuild)
    sqldir = os.path.join (dataroot, dataset, "sql/")
    return sqldir

def getWorkDir(dataset, dataBuild):
    dataroot = getDataRoot("data", dataBuild)
    workdir = os.path.join (dataroot, dataset, "work/")
    return workdir



# Public dataset graphs
CHEMBL_DATA = Namespace ("http://generalbioinformatics.com/data/chembl#")
CHEMBL_VOC = Namespace ("http://generalbioinformatics.com/ontologies/chembl#")


# Internal dataset graphs
CSIM_VOC = Namespace("http://generalbioinformatics.com/ontologies/crossSystemIdMapping#")
CSIM_DATA = Namespace("http://generalbioinformatics.com/data/crossSystemIdMapping#")

MAP_DATA = Namespace ("http://generalbioinformatics.com/data/idMapping#")
MAP_VOC = Namespace ("http://generalbioinformatics.com/ontologies/idMapping#")

PHENOTYPE_DATA = Namespace ("http://generalbioinformatics.com/data/phenotype#")
PHENOTYPE_VOC = Namespace ("http://generalbioinformatics.com/ontologies/phenotype#")

PROJECT_DATA = Namespace ("http://generalbioinformatics.com/data/project#")
PROJECT_VOC = Namespace ("http://generalbioinformatics.com/ontologies/project#")

RELATE_DATA = Namespace ("http://generalbioinformatics.com/data/relate#")
RELATE_VOC = Namespace ("http://generalbioinformatics.com/ontologies/relate#")

