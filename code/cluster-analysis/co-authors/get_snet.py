import os
import sys
import operator
import math
import numpy
import scipy.stats
from operator import itemgetter
import pdb
import networkx as nx
sys.path.append(os.path.realpath('../tna'))
import globalvar
from globalfuncs import *
from analyzer import *


def generate_snet(net_file, vec_file, clu_file)
	netfile = open(net_file, 'r')
	vecfile = open(vec_file, 'r')
	clufile = open(clu_file, 'r')


if __name__ == "__main__":
    communities_directory = os.path.realpath(os.getcwd() + '/../../..')
    setFilePaths(communities_directory)
    generate_snet(argv[0],argv[1],argv[2])