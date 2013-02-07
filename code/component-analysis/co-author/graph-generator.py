import os
import sys
import operator
import numpy
import scipy.stats
from operator import itemgetter
import pdb
import networkx as nx
sys.path.append(os.path.realpath('../../tna'))
import globalvar
from globalfuncs import *
from analyzer import *
from drawer import *

if __name__ == "__main__":
    communities_directory = os.path.realpath(os.getcwd() + '/../../..')
    setFilePaths(communities_directory)
    G = GraphDrawer(communities_directory)
    G.getData(communities_directory + '/parameters/parameters-global.txt')
    G.makeRcomponent()
