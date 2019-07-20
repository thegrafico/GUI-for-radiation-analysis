# brief program description
import os
import statistics      #used to calculate the standard deviation
import pandas as pd
import numpy as np


class Analyze_arg():
	
	def __init__(self):
		self.ar36 = []
		self.ar40 = []
		self.file_names = []

	#===========================================================================================================
	def start(self, path, fname):
		self.fname = fname
		self.file_names.append(fname)
		"""
		start the analysis
		"""
		v = []
		with open(path + self.fname, "r+") as f:
			instrm = f.read().strip()
			
		#instrm = self.get_heading(instrm)
		instrm = instrm.strip()
		instrm = instrm.split('\n')
		
		for i in range(len(instrm)):
			v.append(instrm[i].replace(',','').split())
		#print('FLAG1')
		self.highest(v)
	#===========================================================================================================
	def get_max(self, start, end, x,y):
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
	#===========================================================================================================
	def highest(self, a):
		x = [float(col[0]) for col in a]
		y = [float(colm1[1]) for colm1 in a]
		
		results_ar36 = []
		results_ar40 = []
		results_ar36.append( self.get_max(36,37,x,y))
		results_ar40.append( self.get_max(40,41,x,y))
		
		#creates files from the results
		self.create_a_file(results_ar36, do_ar36=True)
		self.create_a_file(results_ar40, do_ar36=False)
	#===========================================================================================================



	####################################################To write into an export file and calculate standerd deeviation##################################################################################
	#to write values into a text file. Need them to list all from line to line rather than updating it    
	def create_a_file(self, results, do_ar36):
		for result in results:
			a = str(result[0])
			b = str(result[1])
			line = a + ', ' + b
			if do_ar36:
				self.ar36.append(line)
			else:
				self.ar40.append(line)
		# print('FLAG3')

	#===========================================================================================================
	def get_heading(self, text_file):
		end = text_file.find("mAmps")
		return text_file[end + 5:]
		
	#===========================================================================================================   
	def create_data_frame(self):
		columns = ['File', 'Ar_36', 'Ar_40']
		dt = {
		columns[0]: self.file_names,
		columns[1]: self.ar36,
		columns[2]: self.ar40
			}
		return pd.DataFrame(dt)
	
	def get_all_files(self, path):
		files = os.listdir(path)
		files = list(filter(lambda x: x[-4:] == '.txt', files))
		return files
		
	#===========================================================================================================   
def create_dummy_data(n_files):
	"""
	create dummy data
	n_files: number of file to create
	"""
	tam = 300
	for i in range(n_files):
		filename = '.\data\\' + str(i)+ '.txt'
		x = np.random.randint(low=30, high=50, size=tam)
		y = np.random.normal(size=tam)
		with open(filename, 'w+') as f:
			for position in range(tam):		
				pattern = str(x[position]) + ', ' + str(y[position]) + ','
				f.write(pattern + '\n')

#create_dummy_data(10)
#=====================================================================================

data = Analyze_arg()

path = '.\data\\'
files = data.get_all_files(path)

for f in files:
	data.start(path,f)

df = data.create_data_frame()

print(df)

#next steps:
#write code to store all the 36 vals, 40vals, and 40/36 vals all in one new text file
#write the output file elements into a list to run the standerd deviation command through
#set up a designated directory to collect the data from automatically using timestamps
#begin working on interface


"""
	#===========================================================================================================
	def go2(x):
		v = []
		colm2=0
		with open(x, "r+") as f:
			instrm = f.read().strip()
		instrm=instrm.split('\n')
		for i in range(len(instrm)):
			v.append(instrm[i].replace(',','').split())
		highest2(v) 

	#===========================================================================================================    
	def highest2(a):
		x = [float(col[0]) for col in a]
		y= [float(colm1[1]) for colm1 in a]
		print(x)
		print(y)
	 
"""

            

