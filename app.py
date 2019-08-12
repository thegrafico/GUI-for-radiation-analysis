# brief program description
import os
import statistics as st    #used to calculate the standard deviation
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class Analyze_arg():
	
	def __init__(self):
		self.ar36x = []
		self.ar36y = []

		self.ar40x = []
		self.ar40y = []
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
			
		instrm = self.get_heading(instrm)
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
			a = result[0]
			b = result[1]
			# line = a + ', ' + b
			if do_ar36:
				self.ar36x.append(a)
				self.ar36y.append(b)

			else:
				self.ar40x.append(a)
				self.ar40y.append(b)
	#===========================================================================================================
	def get_heading(self, text_file):
		finish = 'mAmps'
		end = text_file.find(finish)
		return text_file[end + len(finish):]
		
	#===========================================================================================================   
	def create_data_frame(self):
		columns = ['File', 'Ar_36_x','Ar_36_y', 'Ar_40_x','Ar_40_y']
		dt = {
		columns[0]: self.file_names,
		columns[1]: self.ar36x,
		columns[2]: self.ar36y,
		columns[3]: self.ar40x,
		columns[4]: self.ar40y
		}
		return pd.DataFrame(dt)
	
	def get_all_files(self, path):
		files = os.listdir(path)
		files = list(filter(lambda x: x[-4:] == '.txt', files))
		return files
		
	def make_calculation(self, df):
			
		df['Ar_40_y'] = df['Ar_40_y'].astype('float64')
		df['Ar_36_y'] = df['Ar_36_y'].astype('float64') 
		df['Y_axis_Ar40_div_Ar36'] = df['Ar_40_y'] /  df['Ar_36_y']

		std_columns = ['Ar_36_x', 'Ar_36_y', 'Ar_40_x', 'Ar_40_y', 'Y_axis_Ar40_div_Ar36']

		df.to_csv('result.txt', header=True, index=False, sep='\t', mode='a')
		
		# result = []
		# for col in std_columns:
		# 	result.append( [col, st.stdev(df[col]] ))
		# 	# print('STD',col,'=',std)
		# return result
	#===========================================================================================================   
	def make_plot(self, df, column):
		# x = df['Ar_36_x'].values
		y = df['Ar_36_y'].values

		# print(x, y)
		_ = plt.boxplot(y)
		plt.xlabel('Pressure')
		plt.ylabel('Counts')
		plt.title('Pressure vs Counts')
		plt.xticks(rotation=45)
		plt.xscale('log')
		plt.grid(True)
		plt.savefig('image.png')
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

if __name__ == '__main__':
		
	data = Analyze_arg()

	# path = '.\data\\'
	path = '.\F350\\'

	files = data.get_all_files(path)

	for f in files:
		data.start(path,f)

	df = data.create_data_frame()

	data.make_calculation(df)

	data.make_plot(df)