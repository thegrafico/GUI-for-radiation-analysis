import os
import pandas as pd
import numpy as np
import sys
import subprocess

class data_cleaning():
	def __init__(self, excel_name):
		try:
			self.df = pd.read_excel(excel_name, header=1)
		except:
			print("Cannot find the file", excel_name, "- So we can't continue with the analysis")
			exit()
		try:				
			self.df = self.df.drop(["Unnamed: 0"],axis=1)
		except:
			print("Can't delete column Unnamed: 0")

		self.df["id_in_data"] = False
		self.df["id_in_report"] = False
		self.df = self.df.rename(columns = {'RRR File (PNNL System)':'RRR_file'})
	
	#-----------------------------------------------------------	
	def create_folders(self):
		try:
			os.mkdir("../data_to_analyze")
		except:
			print("Cannot create a dir")
		
	#-----------------------------------------------------------	
	def get_column(self, column = "SID"):
		"""
		THIS FUNCTION RETURN THE VALUE OF THE COLUMN SID, But you can get any value just change the value of the column
		column: name of the column that you want to. Default: SID
		"""
		return np.array(self.df[column])
	#-----------------------------------------------------------
	def get_all_txt(self, dir_path):
		"""
		Return a list of all txt in a directory
		dir_path: path of the directory. e.g. "~/home/username/dir"
		"""
		try:
			all_files = os.listdir(dir_path)
		except:
			print("Cannot find the directory", dir_path)
			exit()
		if len(all_files) > 0:
			return list(filter(lambda x: x[-4:] == '.txt', all_files))
		else:
			print("There is not file")
			exit()
	#-----------------------------------------------------------
	def get_id_from_txt(self, path = "./data"):
		"""
		The name of the file is the id, so this function return the id (the name without extension)
		path: path of the directory where are all the txt files. Default: ./data
		"""
		txt_files = self.get_all_txt(path)
		if txt_files and len(txt_files) > 0:
			return list(map(lambda x: int(x[:-4]), txt_files))
	#-----------------------------------------------------------
	def convert_all_files_txt_to_data(self, path = "./data", where_to_save = "./data_test/"):
		
		"""
		Convert all the txt files into a data file
		path: where are the txt files stored
		where_to_save: where you want to save all the files
		"""
		
		all_files =  self.get_all_txt(path)
	
		if len(all_files) > 0:	
			for txt_file in all_files:
				filename = txt_file.replace(".txt", ".data")
				with open(path + "/" + txt_file, "r+") as f:
					txt = f.read()
				with open(where_to_save + filename, "w+") as f:
					f.write(txt)
			print("All files where saved at", where_to_save)
	#-----------------------------------------------------------
	def get_id_from_report(self, path_reports = "./2018"):
		"""
		return a list of list with elements with all id find in the final report and the name of the reports that was evaluated
		path_reports: path where all reports files are stored
		"""
		
		
		all_files = self.get_all_txt(path_reports)
		
		if all_files and len(all_files ) > 0:
			
			id_name_from_reports = []
			
			for _file in all_files:
			
				with open(path_reports + "/" + _file, "r+") as f:
					txt = f.read()
					start = txt.find("Sample ID:")
					end = txt.find("Sample Quantity:")
					id_name_from_reports.append([ txt[start:end].split("\n")[0].strip().split()[2], _file])
			
			return id_name_from_reports
		else:
			print("Cannot find any report")
			return None
	#-----------------------------------------------------------
	
	def set_true_is_ids_are_equals(self, id_from_files, id_from_excel, colum_to_compare, column_to_set):
		"""
		This function change the column id_in_data to true if the id math with the id of the dataframe
		id_from_files: list of id that you whant to compera
		id_from_excel: list of id to compare
		colum_to_compare: the dataframe column that you want to compare
		column_to_set: the new column that you are trying to setup
		"""
		
		for _id in id_from_files:
			if _id in id_from_excel:
				self.df.loc[ self.df[colum_to_compare]  == _id, [column_to_set] ] = True
	
		return self.df
	#-----------------------------------------------------------
	def describe(self):
		print(self.df.info())
	
	#-----------------------------------------------------------
	
	def compare(self, in_in_report = "id_in_report", id_in_data = "id_in_data"):
		"""
		This function compare two columns with only booleans values, and then return the dataframe with
		the condition True in both columns
		"""
		conditions = (self.df[in_in_report] == True) & ( self.df[id_in_data] == True )
		
		print("There are", sum(conditions), "Equals Files")
		return self.df[conditions]
	#-----------------------------------------------------------
	def save_to_excel(self, data_frame, path="./cleaned.xlsx", sheetname = "Sheet1" ):
		"""
		save the dataframe into a excel
		path: path where save the file with the name of the file. E.g /home/username/file.xlsx
		sheetname: name of the sheet on excel
		"""	
		try:
			data_frame.iloc[:, :11].to_excel(path, sheet_name=sheetname)
			print("File saved at", path)
		except:
			print("Cannot save the excel file :(")		
		
	#-----------------------------------------------------------
	def convert_from_txt_to_data(self, data_folder, id_from_txt, id_cleaned):
		"""
		Convert the txt files that are already cleaned. Thast mean that only convert to data the txt files
		that have a final report from ctbto
		"""
		count = 0
		text = ""
		
		try:
			os.mkdir("./data_to_analyze")
		except:
			print("Cannot create a dir")
			
		for _id in id_from_txt:
			if _id in id_cleaned:
				try:
					count+=1
					file_path_name = data_folder + "/" + str(_id) + ".txt"
					with open(file_path_name, "r+") as f:
						text = f.read()
						
					file_path_name = "./data_to_analyze/" + str(_id) + ".data"
					with open(file_path_name, "w+") as f:
						f.write(text)	
				except:
					print("Cannot find the directory")
				
		print(count, "files where saved")
					
	#-----------------------------------------------------------
	
#--Start Code
#Columns from reports

def start(maindir, argv1, argv2, argv3):
	#PATH OF THE DATA THAT WE NEED
	rrr_report = argv1
	path_data = argv2
	ctbt_reports = argv3
	
	print("RRR: {}, data: {}, ctbt: {}".format(rrr_report, path_data, ctbt_reports))
	
	##print(rrr_report, path_data, ctbt_reports)
	#dc = data_cleaning(rrr_report)

	#excel_sid = dc.get_column("SID") #default is SID

	##getting data from excel and txt files
	#id_datatxt = dc.get_id_from_txt(path = path_data)
	#id_name_from_report = dc.get_id_from_report(path_reports = ctbt_reports)

	##spliting the id_name_from_report couse is a list of list
	#id_from_report = [int(x[0]) for x in id_name_from_report]
	#name_of_report = [x[1] for x in id_name_from_report] 

	##set true in the excel if id match
	#df = dc.set_true_is_ids_are_equals( id_datatxt, excel_sid,'SID', 'id_in_data')
	#df = dc.set_true_is_ids_are_equals( id_from_report, excel_sid,'SID', 'id_in_report')

	##show how many id that are in the txt, also are in the excel file
	#print("There are", len(df.loc[df["id_in_data"] == True]), "text files to analyze")
	#print("There are", len(df.loc[df["id_in_report"] == True]), "Reports files to analyze")


	##comparing the columns id_in_report with id_in_data
	##from this comparation we get a new dataframe with only the records when both columns are true
	#df_clean = dc.compare(in_in_report = "id_in_report", id_in_data = "id_in_data")


	##saving the new dataframe into a new excel file
	#dc.save_to_excel(df_clean)


	##convert the txt values from the new dataframe
	#dc.convert_from_txt_to_data(path_data, id_datatxt, list(df_clean.SID))

	subprocess.call('{}/.pipeline.sh'.format(maindir))
	#os.system('source {}/.pipeline.sh'.format(maindir))
	#os.system('run_pipeline')
	

#print(id_datatxt)
#print(list(df_clean.SID))
#id_seven_char =  sum( [len( str(x) ) for x in id_from_report] ) / 7
#--End Code
