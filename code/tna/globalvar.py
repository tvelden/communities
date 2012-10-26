import os
import sys
import operator
import numpy
import scipy.stats
from operator import itemgetter
import pdb
import networkx as nx
import globalvar

#--Global Variables--
RELATIVE_INPUT_PARAMETER_FILE = ''
INPUT_PARAMETER_FILE = ''
INPUT_ORIGINAL_FILE_PATH = ''
INPUT_REDUCED_FILE_PATH = ''
OUTPUT_PARENT_DIRECTORY_PATH = ''
OUTPUT_NETWORK_DIRECTORY_FOR_PAJEK = ''
OUTPUT_STATISTICS_DIRECTORY = ''
OUTPUT_NETWORK_DIRECTORY_FOR_COMPONENTS = ''
OUTPUT_STATISTICS_DIRECTORY_FOR_COMPONENTS = ''
FIELD = ''
RUN = ''
START_YEAR = 0
END_YEAR = 0
TYPE = ''
SIZE = 0
