from tkinter import *
import sys
sys.path.insert(1, './scrits')
from tkinter import ttk
from tkinter.ttk import *
from tkinter import filedialog
from tkinter import messagebox as msg_box
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import clean_data
import make_analysis as mk
import pandas as pd
import numpy as np
import os
from tkinter import simpledialog

class Root(Tk):
	def __init__(self):
		super(Root, self).__init__()
		self.title('IMS Data Analisys')
		self.width = self.winfo_screenwidth() - 100
		self.height = self.winfo_screenheight()
		self.minsize(self.width, self.height)
		#self.maxsize(self.width //2,self.height//2)
		
		self.filepath = ''
		self.rrr_report = ''
		self.ctbt_reports = ''
		
		#self.resizable(width=0, height=0)
		self.maindir = os.path.dirname(os.path.realpath(__file__))
		self._create_folders()
		#self.wm_iconbitmap(self.maindir + '/' + 'rad.ico')
		self.std_logfolder = 'std_log.txt'
		#self._create_folders()
		self.show_menu()
		
		self.run_one_time = True
		self.table()
		#self.standar_table()
		#self.table()
#============================================================================   
	def _create_folders(self):
		"""
		Create a directory if dosen't exits
		"""
		directorys = ["/data_to_analyze","/report_autoSaint" ]	
		for d in directorys:
			direc = self.maindir + d
			if not os.path.exists(direc):
				os.makedirs(direc)
#============================================================================   
	def button(self):
		"""
		Browse a file into the user directory interface
		"""
		self.button = ttk.Button(self.labelFrame, text='Browse A File', command=self.select_directory)
		self.button.grid(column=1, row=1)
#============================================================================   
	def select_directory(self):
		"""
		option to select the folder to work
		"""
		self.filepath = filedialog.askdirectory(initialdir='/home', title='Select folder with raw data', mustexist=False)
		
		self.activate_pipeline()
		if self.filepath and self.filepath != '':
			self.activate_pipeline()
			#files = self.code.get_all_files(self.filepath)
			#self.do_analysis(self.filepath + '/', files)
			#self.fill_std()
			#self.matplotlib_canvas()
#============================================================================
	def select_rrr_report(self):
		self.rrr_report = filedialog.askopenfilename(initialdir='/home', title='Select RRR report')
		if self.rrr_report and self.rrr_report != '':
			self.activate_pipeline()
		
	def select_ctbt_report(self):
		self.ctbt_reports = filedialog.askdirectory(initialdir='/home', title='Select Folder with CTBTO reports', mustexist=False)	
		if self.ctbt_reports and self.ctbt_reports != '':
			self.activate_pipeline()
#===================================ACTIVATE THE PIPELINE=========================================
	def activate_pipeline(self):
		if self.run_one_time:
			self.show_label(" ")
			self.excel_file_name = "clean.xlsx"
			self.df = mk.start_analysis(self.excel_file_name, self.maindir)
			self.table()
			if self.filepath and self.rrr_report and self.ctbt_reports:
				##Step1
				#self.progress_bar("Analyzing data...")
				#self.incremment_bar(20)
				#clean_data.step1(self.maindir, self.rrr_report, self.filepath , self.ctbt_reports, self.excel_file_name)
				
				##Generating reports
				#self.update_label("Generating reports...")
				#self.incremment_bar(40)
				#clean_data.step2(self.maindir, self.rrr_report, self.ctbt_reports)
				
				#analyze reports
				self.incremment_bar(80)
				self.update_label("Comparing reports...")
				mk.start_analysis(self.excel_file_name)
				
				##END
				self.incremment_bar(100)
				self.update_label("Done!")
			print("DONE")
			self.run_one_time = False
#============================================================================
	def donothing(self):
		filewin = Toplevel(self)
		self.button = Button(filewin, text="Do nothing button")
		self.button.pack()
#============================================================================

	def show_label(self, texto):
		self.progress_label = ttk.Label(self, text=texto, font=("Arial",30))
		self.progress_label.pack()
		
	def progress_bar(self):		
		self.progress = Progressbar(self,orient=HORIZONTAL,length= self.width // 3, mode='determinate')
		self.progress.place(x=(self.width // 2) - (self.width // 3) // 2, y= self.height - (self.height * 0.9) )
	
	def incremment_bar(self, increment):
		self.progress['value']=increment
		self.update_idletasks()
	
	def update_label(self, texto):
		self.progress_label.configure(text=texto)
		self.progress_label.update()
#============================================================================
	def show_menu(self):
		# root = Tk()
		menubar = Menu(self)

		#file menu
		filemenu = Menu(menubar, tearoff=0)
		filemenu.add_command(label="Select RRR report", command=self.select_rrr_report)
		filemenu.add_command(label="Select Directory with raw data", command=self.select_directory)
		filemenu.add_command(label="Select Directory with reports CTBTO", command=self.select_ctbt_report)
		filemenu.add_separator()
		filemenu.add_command(label="Exit", command=self.quit)
		menubar.add_cascade(label="File", menu=filemenu)

		#Options menu
		editmenu = Menu(menubar, tearoff=0)
		editmenu.add_command(label="Remove std values", command=self.donothing)
		editmenu.add_command(label="Select New Range", command=self.popup_input)
		menubar.add_cascade(label="options", menu=editmenu)

		#help menu
		helpmenu = Menu(menubar, tearoff=0)
		helpmenu.add_command(label="Help Index", command=self.donothing)
		helpmenu.add_command(label="About...", command=self.donothing)
		menubar.add_cascade(label="Help", menu=helpmenu)

		self.config(menu=menubar)
#============================================================================   
	#def do_analysis(self, path, files):
		#"""
		#Calculate the std for all columns
		#"""
		#for f in files:
			#self.code.start(path,f)

		#self.df = self.code.create_data_frame()
		
		#self.ratio = self.get_ratio()
		#self.fill_values_table()
		
		#self.code.make_calculation(self.df)
# #============================================================================   
	def fill_values_table(self):
		# File,Ar_36_x,Ar_36_y,Ar_40_x,Ar_40_y,Y_axis_Ar40_div_Ar36
		values = list(zip(self.df['File'].values, self.df['Ar_36_x'].values,
		self.df['Ar_36_y'].values, self.df['Ar_40_x'].values,
		self.df['Ar_40_y'].values, self.ratio))
	 
		for i, (filename, ar36x, ar36y, ar40x, ar40y, ratio) in enumerate(values, start=1):
			self.listBox.insert("", "end", values=(filename, ar36x, ar36y, ar40x, ar40y, "{:.2e}".format(ratio)))
# #============================================================================   
	def fill_std(self):
		# File,Ar_36_x,Ar_36_y,Ar_40_x,Ar_40_y,Y_axis_Ar40_div_Ar36
		cols =  ['Ar_36_x', 'Ar_36_y', 'Ar_40_x', 'Ar_40_y', 'Ratio(Ar36_y / Ar40_y)']
		std = self.calculate_std(cols)
		name = self.get_name(self.filepath.strip())
		self.stdBox.insert("", "end", values=(name, "{:.2e}".format(std[0]), "{:.2e}".format(std[1]), "{:.2e}".format(std[2]),
		 "{:.2e}".format(std[3]), "{:.2e}".format(std[4])))
		self.save_std_log(name, std)
# #============================================================================   
	def table(self):
		"""
		Table of values from directory
		"""
		self.show_label(" ")
		self.update_label("Results")
		#label = Label(self, text="Values", font=("Arial",30)).pack()
		# create Treeview with 3 columns
		
		columns = ["Station ID", "Nuclide", "Conc. (uBq/m3)", "Station Location", "SID",
		 "ENERGY", "CENTROID", "FWHM", "AREA", "AREA_ERR", "DET", "EFFICIENCY", "EFF_ERROR",
		 "NAME", "KEY_ACTIV","ERR", "AVE_ACTIV", "ERR_", "MIN_MDA"]
		cols = columns

		self.listBox = ttk.Treeview(self, columns=cols, show='headings')  
		self.listBox.place(x=self.width * 0.02, y= self.height * 0.05,
		 width= self.width - (self.width * 0.04), height = self.height - (self.height * 0.20))
		
		#Scroolbar
		vsb = ttk.Scrollbar(self, orient="vertical", command=self.listBox.yview)
		vsb.place(x=self.width - (self.width * 0.02), y= self.height * 0.09, height= self.height - (self.height * 0.25))
		
		vsb2 = ttk.Scrollbar(self, orient="horizontal", command=self.listBox.xview)
		vsb2.place(x=self.width * 0.02, y= self.height - (self.height * 0.15), width= self.width - (self.width * 0.04))
		
		
		self.listBox.configure(yscrollcommand=vsb.set, xscrollcommand=vsb2.set)

		
		# set column headings
		for i,col in enumerate(cols):
			self.listBox.heading(col, text=col)
			self.listBox.column(str(i), width= 120 )    
# #============================================================================   
	def matplotlib_canvas(self):
		"""
		Create the grapth to show into the GUI
		"""
		f = Figure(figsize=(7,7), dpi=70)
		names = self.get_files_names()
		index1, index2 = len(self.df['File'].values) // 2, len(self.df['File'].values) -1
		#fig 1
		a = f.add_subplot(211)
		a.plot(self.df['File'].values, self.ratio )
		a.set_xticks([0,index1, index2])
		a.set_xticklabels([names[0], names[index1],names[index2]])
		a.set_xlabel('Time')
		a.set_title('Time vs Ratio')
		a.set_ylabel('Ratio')
		# #fig 2
		b = f.add_subplot(212)
		b.hist(self.ratio)
		b.set_title('Ratio frequency')
		b.set_xlabel('Ratio (Ar36_y / Ar40_y)')
		b.set_ylabel('Counts')
		b.set_xscale('log') 
		
		f.tight_layout()
		canvas = FigureCanvasTkAgg(f,self)
		canvas.draw()
		canvas.get_tk_widget().place(x=self.width//1.7, y=self.height//3)
	# #============================================================================   
	def calculate_std(self, col):
		"""
		Calculate the standard deviation 
		"""
		result = []
		for x in col:
			result.append(st.stdev(self.df[x].values))
		# print(result)
		return result
# #============================================================================   
	def standar_table(self):

		# create Treeview with 3 columns
		cols = ('Folder', 'Ar36_x', 'Ar36_y', 'Ar40_x', 'Ar40_y', 'Ratio(Ar36_y / Ar40_y)')
		# set column headings
		label = Label(self, text="Standard Deviation", font=("Arial",30)).place(x= self.width//(len(cols)+3), y =self.height//2.8)

		self.stdBox = ttk.Treeview(self, columns=cols, show='headings')  
		self.stdBox.place(x=20, y=self.height//2.4)

		for i,col in enumerate(cols):
			self.stdBox.heading(col, text=col)
			if i == 0:
				self.stdBox.column(str(i), width=(self.width//(len(cols)+10)), anchor='c')    
			else:
				self.stdBox.column(str(i), width=(self.width//(len(cols)+5)), anchor='c') 
		
		showScores = ttk.Button(self, text="Load STD", width=15, command=self.load_std_from_log).place(x=self.width//2.5, y=self.height //1.45)
# #============================================================================   
	def load_std_from_log(self):
		"""
		load all std from log files and display into the table STD in the GUI
		"""
		try:
			with open(self.maindir + '\\stdlog\\' + self.std_logfolder, 'r+') as f:
				info = f.read().strip().split('\n')
		except:
			self.message_box('Missing file', 'Log file not found')
			return
		data = []
		for v in info:
			data.append(v.split(','))
		for v in data:
			self.stdBox.insert("", "end", values=(v[0], v[1], v[2], v[3], v[4]))

# #============================================================================   
	def get_name(self, pathdir):
		"""
		Get the name of the folder that we are analyzing
		"""
		name = []
		for i in range(len(pathdir) - 1, 0, -1):
			if pathdir[i] == '/' or pathdir[i]=='\\':
				break
			else:
				name.append(pathdir[i])
		return "".join(name[::-1])
# #============================================================================       
	def save_std_log(self, filename, std):   
		with open(self.maindir + '\\stdlog\\' + self.std_logfolder, 'a+') as f:
			f.write(filename + ',')
			for value in std:
				f.write(str(value) +',')
			f.write('\n')
			print('std was saved')
# #============================================================================   
	def message_box(self, title, mesj):
		msg_box.showinfo(title, mesj)

	def warning_box(self, title, mesj):
		msg_box.showwarning(title, mesj)

	def error_box(self, title, mesj):
		msg_box.showerror(title, mesj)
# #============================================================================   
	def popup_input(self):
		answer = simpledialog.askstring("\nInput", "Please Enter the range.\nFormat: start:end (Eg. 36:40)\n", parent=self)
		print(answer, type(answer))
# #============================================================================   
	def get_ratio(self):
		self.df['Ratio(Ar36_y / Ar40_y)'] = self.df['Ar_36_y'] / self.df['Ar_40_y']
		return self.df['Ratio(Ar36_y / Ar40_y)'].values 
# #============================================================================   
	def get_files_names(self):
		names = []
		for filename in self.df['File']:
			names.append(filename[-15:-4])
		return names
# #============================================================================   
if __name__ == '__main__':
	root = Root()
	root.mainloop()
