# brief program description
import os
import statistics      #used to calculate the standard deviation
import pandas as pd
import numpy as np


def get_max(start, end, x,y):  
    l = []
    for xx,yy in zip(x,y):
        if xx >= start and xx < end:
            l.append(yy)
            
    mx = max(l)
    for xx,yy in zip(x,y):
        if xx >= start and xx < end:
            if yy == mx:
                return [xx,yy]
                
                #print(statistics.stdev([xx,yy]))    #this is to calculate the standard deviation
def highest(a):
    x = [float(col[0]) for col in a]
    y= [float(colm1[1]) for colm1 in a]
    
    results = []
    results.append( get_max(36,37,x,y))
    results.append( get_max(40,41,x,y))
    
    create_a_file(results)
def go(x):
    v = []
    colm2=0
    with open(x, "r+") as f:
        instrm = f.read().strip()
    instrm=instrm.split('\n')
    for i in range(len(instrm)):
        v.append(instrm[i].replace(',','').split())
    highest(v)  
####################################################To write into an export file and calculate standerd deeviation##################################################################################
#to write values into a text file. Need them to list all from line to line rather than updating it    
def create_a_file(results):
    fout= open('Output','w')
    for result in results:
        a = str(result[0])
        b = str(result[1])
        line = a + ', ' + b + '\n'
        fout.write(line)
    fout.close()
    
def go2(x):
    v = []
    colm2=0
    with open(x, "r+") as f:
        instrm = f.read().strip()
    instrm=instrm.split('\n')
    for i in range(len(instrm)):
        v.append(instrm[i].replace(',','').split())
    highest2(v) 
    
def highest2(a):
    x = [float(col[0]) for col in a]
    y= [float(colm1[1]) for colm1 in a]
    print(x)
    print(y)
    

go('')

#next steps:
#write code to store all the 36 vals, 40vals, and 40/36 vals all in one new text file
#write the output file elements into a list to run the standerd deviation command through
#set up a designated directory to collect the data from automatically using timestamps
#begin working on interface


            

