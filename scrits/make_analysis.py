import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

col_report_rms = ["ENERGY", "CENTROID", "FWHM", "AREA", "AREA_ERR", "DET", "EFFICIENCY", "EFF_ERROR"]
col_report_rms_isotopes = ["NAME", "KEY_ACTIV","ERR", "AVE_ACTIV", "ERR_", "MIN_MDA"]
col_report_rrr = ["Energy_(keV)","Centroid","Width", "FWHM_(keV)", "Eff_(%)", "Area", "Bkgnd_(%)", "RelErr_(%)", "Nuclide", "Nts"]
maindir = os.path.dirname(os.path.realpath(__file__))
#----------------------------------------------------------------------
def set_up_columns(columns, values, excel, position):
	#print(columns)
	#print(values)
	result = zip(columns, values)
	
	for col,val in result:
		excel.loc[excel[col].index == position, col] = val

#----------------------------------------------------------------------
def get_index(raw_text, nuclide):
	index = None
	for i,e in enumerate(raw_text):
		if nuclide in e:
			index = i
	if not index:
		raise Exception("cannot find the index")
	return index 
	
#----------------------------------------------------------------------
def get_important_data(raw_data, pattern_start, pattern_end):
	try:
		start = raw_data.find(pattern_start)
		end = raw_data.find(pattern_end)
		txt = raw_data[start:end].split('\n')
		return txt
	except:
		print("cannot find the pattern in the file")
#----------------------------------------------------------------------
def open_file(file_name, autosain_path):
	try:
		n = autosain_path + "/" + str(file_name) + ".data.txt"
		#print("FIND THE FILE HERE", n)
		with open(n, "r+") as f:
			return f.read()
	except:
		print("Cannot find the file")
		return False
#----------------------------------------------------------------------

def get_file_raw_data(excel, autosain_path):
	
	for position in range(len(excel["SID"])):
		
		fname = excel.loc[ excel["SID"].index == position, "SID"].values[0]
		nuclide =  excel.loc[ excel["Nuclide"].index == position, "Nuclide"].values[0]
		print("NAME",fname)
		raw_data = open_file(fname, autosain_path)

		if not raw_data:
			continue
			
		data= get_important_data(raw_data,"Peaks identification:", "Final Peak Search summary:")

		try:
			index = get_index(data, nuclide)
		except:
			#TODO: Fill up the empty data
			#print("Nuclide miss =>", nuclide, "|| in the file =>", str(fname) + ".data")	
			data = get_important_data(raw_data,"Isotopes:", "End activities calculation")
			for row in data:
				if nuclide in row:
					set_up_columns(col_report_rms_isotopes, row.strip().split(), excel, position)
			continue
		
		data = get_important_data(raw_data,"Found peaks:", "End peak search")
			
		#print(data[index].strip().split())
		#column = data[1].strip()
		
		
		#giving values to the columns	
		set_up_columns(col_report_rms, data[index].strip().split()[1:], excel, position)
		
		data = get_important_data(raw_data,"Isotopes:", "End activities calculation")

		for row in data:
			if nuclide in row:
				#print(row.strip().split())
				set_up_columns(col_report_rms_isotopes, row.strip().split(), excel, position)
#----------------------------------------------------------------------
def compare_MIN_MDA(excel):
	excel["MIN_MDA"] = excel["MIN_MDA"].astype('float64') 
	
	uBq = np.array(excel["Conc. (uBq/m3)"])
	min_md =  np.array(excel["MIN_MDA"])
	
	comparation = min_md >= uBq 
	
	excel["MIN_MD_vs_Conc.(uBq/m3)"] = comparation 
	excel["MIN_MD_vs_Conc.(uBq/m3)"] = excel["MIN_MD_vs_Conc.(uBq/m3)"].apply(lambda x: 'EXPECTED' if x else 'WARNING')
	
	#print(excel["MIN_MD_vs_Conc.(uBq/m3)"])
#----------------------------------------------------------------------
def clean_name(names):
	l = []
	for n in names:
		le = n
		if len(n) > 19:
			first_name = n.split(',')
			if len(first_name) > 2:
				hay_tres = True
			city_name = first_name[0]
			#print(first_name, 'City =>', city_name)
			seconds_letter= first_name[1].strip().split(' ')
			if len(seconds_letter) == 1:
				le = city_name + ', ' + seconds_letter[0][:3]
			elif len(seconds_letter) > 2:
				le = city_name + ', ' + seconds_letter[0][:3]
			else:
				le = city_name + ', ' + seconds_letter[0][:3] + '-' + seconds_letter[1][:2]
				
		l.append(le)
	return l
def station_location_freq(excel):
	
	expected = excel['MIN_MD_vs_Conc.(uBq/m3)'] == 'EXPECTED'
	warning = excel['MIN_MD_vs_Conc.(uBq/m3)'] == 'WARNING'
	font_title = 32
	font_letter = 30
	#expect = excel[expected]
	warning = excel[warning]
	nuclide = warning['Nuclide'].value_counts() 
	data = warning['Station Location'].value_counts()
	#print(data.values)
	names = data.index
	names = clean_name(names)
	
	#plt.figure(1)
	plt.rcParams["figure.figsize"] = [28,20]
	ax = plt.gca()
	plt.barh(names[:10], data.values[:10], height=0.4, align='center')
	plt.xlabel('Counts', fontsize=font_letter)
	plt.ylabel('Stations Location', fontsize=font_letter)
	ax.invert_yaxis()
	plt.title('Stations with MDA below expected', fontsize=font_title)
	plt.xticks(rotation=65, fontsize=font_letter)
	plt.yticks(fontsize=font_letter)
	plt.grid(True)

	plt.savefig('Stations.png')

def data_for_table(data_frame):
	columns = ["Station ID", "Nuclide", "Conc. (uBq/m3)", "Station Location", "SID",
	 "ENERGY", "CENTROID", "FWHM", "AREA", "AREA_ERR", "DET", "EFFICIENCY", "EFF_ERROR",
	 "NAME", "KEY_ACTIV","ERR", "AVE_ACTIV", "ERR_", "MIN_MDA"]
	return data_frame[columns]
#----------------------------------------------------------------------
def start_analysis(excel_name, maindir):
	excel_filename = excel_name
	excel_filename_after_comparte = '/Analisys.xlsx'
	autosain_dir = maindir + "/report_autoSaint"
	try:	
		df = pd.read_excel(excel_filename)
	except:
		print('File not found:', excel_filename)
		exit()

	df.reset_index()
	
	for col in col_report_rms:
		df[col] = "n/a"

	for col in col_report_rms_isotopes:	
		if col == 'MIN_MDA':
			df[col] = 0
		else:
			df[col] = "n/a"

	get_file_raw_data(df, autosain_dir)
	
	compare_MIN_MDA(df)
	
	df.to_excel(maindir + excel_filename_after_comparte )
	
	return data_for_table(df)
