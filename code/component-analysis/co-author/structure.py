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
from getcomponents import *


def getStructure():
	fsd = globalvar.OUTPUT_NETWORK_DIRECTORY_FOR_COMPONENTS
	
	output2 = fsd + '/' + str(globalvar.FIELD) + str(globalvar.RUN) + '_' + str(globalvar.TYPE) + str(globalvar.START_YEAR) + '-' + str(globalvar.END_YEAR) + '_' + str(globalvar.SIZE) + 'years_LargestComponent_structure.net'
	foutput2 = open(output2,'w')
	foutput2.write('Start_Year; End_Year; Size; Size_Fraction; From_Unborn; From_Unbron_Fraction; Unborns_Fraction\n')
	
	output3 = fsd + '/' + str(globalvar.FIELD) + str(globalvar.RUN) + '_' + str(globalvar.TYPE) + str(globalvar.START_YEAR) + '-' + str(globalvar.END_YEAR) + '_' + str(globalvar.SIZE) + 'years_OtherComponent_structure.net'
	foutput3 = open(output3,'w')
	foutput3.write('Start_Year; End_Year; Size; Size_Fraction; From_Unborn; From_Unbron_Fraction; Unborns_Fraction\n')
	
	newunborn = fsd + '/' + str(globalvar.FIELD) + str(globalvar.RUN) + '_' + str(globalvar.TYPE) + str(globalvar.START_YEAR) + '-' + str(globalvar.END_YEAR) + '_' + str(globalvar.SIZE) + 'years_Unborn_component_structure.net'
	fnewunborn = open(newunborn, 'w')
	fnewunborn.write('Start_Year; End_Year; Size; Size_Fraction; From_Unborn; From_Unbron_Fraction; Unborns_Fraction\n')
	fnub2 = fnewunborn
	
	if(globalvar.TYPE == 'discrete' or globalvar.TYPE == 'accumulative' or globalvar.TYPE == 'sliding'):
		start = globalvar.START_YEAR
		end = start + globalvar.SIZE -1
		old_start = start
		old_end = end
		sflag = 0
		while(end<=globalvar.END_YEAR):
			complist = fsd + '/' + str(start) + '-' + str(end)  + '/components/pajek' + '/' + str(globalvar.FIELD) + str(globalvar.RUN) + '_' + str(globalvar.TYPE) + str(start) + '-' + str(end) + '_' + str(globalvar.SIZE) + 'years_components.net'
			fcomplist = open(complist, 'r')
			
			newunborn = fsd + '/' + str(start) + '-' + str(end)  + '/components/pajek' + '/' + str(globalvar.FIELD) + str(globalvar.RUN) + '_' + str(globalvar.TYPE) + str(start) + '-' + str(end) + '_' + str(globalvar.SIZE) + 'years_unborn.net'
			fnewunborn = open(newunborn, 'r')
			newunborns = []
			for line in fnewunborn:
				if(line[0]=='*'):
					continue
				newunborns.append(line[0:len(line)-1])
			newunbornsize = len(newunborns)
			
			fnewunborn = fnub2
			
			print '********'
			print start
			print end
			print '********'
			

			components = {}
			compstart = 0
			for line in fcomplist:
				if(compstart == 0 and line[0]!= '*'):
					continue
				if(line == '\n'):
					continue
				compstart = 1
				if(line[0]=='*' and line[1]=='C'):
					#print line
					cnumber = int(line[11:len(line)-1])
					#print cnumber
					components[cnumber] = []
					continue
				if(line[0] =='*' and line[1] =='*'):
					csize = int(line[6:len(line)-1])
					continue
				components[cnumber].append(line[0:len(line)-1])
			
			sz = 0
			for e in components:
				sz = sz + len(components[e])
			if(sz==0):
				sz = 1
			othersize = sz - len(components[1])
			
			if(sflag == 0):
				foutput2.write(str(start) + '; ' + str(end) + '; ' + str(len(components[1])) + '; ' + str(float(len(components[1]))/float(sz)) + '; ' + '0; 0; 0\n')
				foutput3.write(str(start) + '; ' + str(end) + '; ' + str(othersize) + '; ' + str(float(othersize)/float(sz)) + '; ' + '0; 0; 0\n')
				fnewunborn.write(str(start) + '; ' + str(end) + '; ' + str(newunbornsize) + '; ' + str(float(newunbornsize)/float(sz)) + '; ' + '0; 0; 0\n')
				old_start = start
				old_end = end
				start = end + 1
				end = end + globalvar.SIZE
				sflag = 1
				fcomplist.close()
				continue
				
			unborn = fsd + '/' + str(old_start) + '-' + str(old_end)  + '/components/pajek' + '/' + str(globalvar.FIELD) + str(globalvar.RUN) + '_' + str(globalvar.TYPE) + str(old_start) + '-' + str(old_end) + '_' + str(globalvar.SIZE) + 'years_unborn.net'
			print unborn
			funborn = open(unborn, 'r')
			
			unborns = []
			for line in funborn:
				if(line[0]=='*'):
					continue
				unborns.append(line[0:len(line)-1])
			unbornsize = len(unborns)
			print 'unborn size is:'
			print unbornsize
			
			
			cunborns = 0
			for e in newunborns:
				if e in unborns:
					cunborns = cunborns + 1
						
			output = fsd + '/' + str(start) + '-' + str(end)  + '/components/pajek' + '/' + str(globalvar.FIELD) + str(globalvar.RUN) + '_' + str(globalvar.TYPE) + str(start) + '-' + str(end) + '_' + str(globalvar.SIZE) + 'years_component_structure.net'
			foutput = open(output,'w')
			
			
				
			foutput.write('Start_Year; End_Year; Component_No; Size; Size_Fraction; From_Unborn; From_Unbron_Fraction; Unborns_Fraction\n')
			estart = 0
			tcount1 = 0
			tcount2 = 0
			for e in components:
				if(estart==0):
					#print start, end
					foutput2.write(str(start)+'; '+str(end)+'; '+str(len(components[e])) + '; '+ str(float(len(components[e]))/float(sz)) + ';')
				
				#print start, end
				foutput.write(str(start)+'; '+str(end)+'; '+ str(e)+'; '+str(len(components[e])) + '; ')
				count = 0
				for element in components[e]:
					if element in unborns:
						count = count + 1
				
				
				lnew = len(components[e])
				if(lnew ==0):
					lnew = 1
				if(unbornsize ==0):
					unbornsize =1
				#print count
				foutput.write(str(float(len(components[e]))/float(sz)) + '; ' + str(count)+ '; '+ str(float(count)/float(lnew))+ '; ' + str(float(count)/float(unbornsize)) + '\n')
				if(estart ==1):
					tcount1 = tcount1 + len(components[e])
					tcount2 = tcount2 + count
				#print count
				if(estart == 0):
					foutput2.write(str(count) + '; ' + str(float(count)/float(len(components[e])))+ '; ' + str(float(count)/float(unbornsize)) + '\n')
					estart = 1
					
			foutput3.write(str(start)+'; '+str(end)+'; '+str(tcount1) + '; '+str(float(tcount1)/float(sz)) + '; '+str(tcount2) + '; '+ str(float(tcount2)/float(tcount1))+ '; ' + str(float(tcount2)/float(unbornsize)) +'\n')
			
				#print e,len(components[e]),count,float(count)/float(len(components[e]))
			
			
			
			nubsz = newunbornsize
			if(nubsz ==0):
				nubsz =1
			fnewunborn.write(str(start) + '; ' + str(end) + '; ' + str(newunbornsize) + '; ' + str(float(newunbornsize)/float(sz)) + '; ' + str(cunborns) + '; ' + str(float(cunborns)/float(nubsz)) + '; ' + str(float(cunborns)/float(unbornsize)) + '\n')
			
				
			fcomplist.close()
			funborn.close()
			old_start = start
			old_end = end
			start = end + 1
			end = end + globalvar.SIZE
			
		foutput2.close()
		foutput3.close()
		fnewunborn.close()
		
		output2 = fsd + '/' + str(globalvar.FIELD) + str(globalvar.RUN) + '_' + str(globalvar.TYPE) + str(globalvar.START_YEAR) + '-' + str(globalvar.END_YEAR) + '_' + str(globalvar.SIZE) + 'years_LargestComponent_structure.net'
		foutput2 = open(output2,'r')
		
		output3 = fsd + '/' + str(globalvar.FIELD) + str(globalvar.RUN) + '_' + str(globalvar.TYPE) + str(globalvar.START_YEAR) + '-' + str(globalvar.END_YEAR) + '_' + str(globalvar.SIZE) + 'years_OtherComponent_structure.net'
		foutput3 = open(output3,'r')
		
		newunborn = fsd + '/' + str(globalvar.FIELD) + str(globalvar.RUN) + '_' + str(globalvar.TYPE) + str(globalvar.START_YEAR) + '-' + str(globalvar.END_YEAR) + '_' + str(globalvar.SIZE) + 'years_Unborn_component_structure.net'
		fnewunborn = open(newunborn, 'r')
		
		growth = fsd + '/' + str(globalvar.FIELD) + str(globalvar.RUN) + '_' + str(globalvar.TYPE) + str(globalvar.START_YEAR) + '-' + str(globalvar.END_YEAR) + '_' + str(globalvar.SIZE) + 'years_Unborn_component_growth.net'
		fgrowth = open(growth, 'w')
		fgrowth.write('Type; Start_Year; End_Year; Size; Size_Fraction; From_Unborn; From_Unbron_Fraction; Unborns_Fraction\n')
		
		
		for line in foutput2:
			if(line[0]=='S'):
				continue
			fgrowth.write('L; ' + str(line))
		foutput2.close()
		for line in foutput3:
			if(line[0]=='S'):
				continue
			fgrowth.write('O; ' + str(line))
		foutput3.close()
		for line in fnewunborn:
			if(line[0]=='S'):
				continue
			fgrowth.write('U; ' + str(line))
		fnewunborn.close()
		fgrowth.close()
		


if __name__ == "__main__":
	communities_directory = os.path.realpath(os.getcwd() + '/../../..')
	setFilePaths(communities_directory)
	makeComponents()
	getStructure()
