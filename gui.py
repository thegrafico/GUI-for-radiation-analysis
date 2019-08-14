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
		self.excel_file_name = "clean.xlsx"
		if self.run_one_time:
			if self.filepath and self.rrr_report and self.ctbt_reports:
				
				print("STAR ANALYSIS")
				#Step1
				#CLEANING THE DATA
				self.show_label("Analyzing data...")
				self.progress_bar()
				self.incremment_bar(20)
				clean_data.step1(self.maindir, self.rrr_report, self.filepath , self.ctbt_reports, self.excel_file_name)
				
				#STEP2
				#Generating reports
				self.update_label("Generating reports...")
				self.incremment_bar(40)
				clean_data.step2(self.maindir, self.rrr_report, self.ctbt_reports)
				
				#STEP3
				#analyzing reports
				self.incremment_bar(80)
				self.update_label("Comparing reports...")
				self.df = mk.start_analysis(self.excel_file_name, self.maindir)
				self.update_label("Results")
				self.table()
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
		editmenu.add_command(label="Analyze Reports", command=self.analyze_folder_autosain)
		editmenu.add_command(label="Save Results as excel file", command=self.popup_input)
		menubar.add_cascade(label="options", menu=editmenu)

		#help menu
		helpmenu = Menu(menubar, tearoff=0)
		helpmenu.add_command(label="Help Index", command=self.donothing)
		helpmenu.add_command(label="About...", command=self.donothing)
		menubar.add_cascade(label="Help", menu=helpmenu)

		self.config(menu=menubar)
#============================================================================   
	def fill_values_table(self, col):
			
		values = list(zip(self.df[col[0]].values, self.df[col[1]].values,self.df[col[2]].values,
		self.df[col[3]].values,self.df[col[4]].values,self.df[col[5]].values,self.df[col[6]].values,
		self.df[col[7]].values,self.df[col[8]].values, self.df[col[9]].values,self.df[col[10]].values,
		self.df[col[11]].values,self.df[col[12]].values,self.df[col[13]].values,self.df[col[14]].values,
		self.df[col[15]].values,self.df[col[16]].values, self.df[col[17]].values,self.df[col[18]].values, self.df[col[19]].values))
	 
		for i, (x1,x2,x3,x4,x5,x6,x7,x8,x9,x10,x11,x12,x13,x14,x15,x16,x17,x18,x19, x20) in enumerate(values):
			col_tag = self.toggle_color(i)
			
			if x1 == "BELOW":
				self.listBox.insert("", "end", values=(x1,x2,x3,x4,x5,x6,x7,x8,x9,x10,x11,x12,x13,x14,x15,x16,x17,x18,x19, x20), tags = ("warning",))
			else:	
				self.listBox.insert("", "end", values=(x1,x2,x3,x4,x5,x6,x7,x8,x9,x10,x11,x12,x13,x14,x15,x16,x17,x18,x19, x20), tags = (col_tag,))
	
		#self.listBox.tag_configure('oddrow', background='gray')
		self.listBox.tag_configure('warning', background='orange')
# #================================TABLE============================================  

	def toggle_color(self, n):
		if n%2 == 0:
			return "evenrow"	
		return "oddrow" 
			 
	def table(self):
		"""
		Table of values from directory
		"""
		self.show_label(" ")
		self.update_label("Results")
		#label = Label(self, text="Values", font=("Arial",30)).pack()
		# create Treeview with 3 columns
		
		columns = ["MDA_vs_Conc.(uBq/m3)", "MIN_MDA", "Conc. (uBq/m3)",  "Nuclide","Station Location", "SID",
		 "ENERGY", "CENTROID", "FWHM", "AREA", "AREA_ERR", "DET", "EFFICIENCY", "EFF_ERROR",
		 "NAME", "KEY_ACTIV","ERR", "AVE_ACTIV", "ERR_", "Station ID"]

		self.listBox = ttk.Treeview(self, columns=columns, show='headings', height=20)  
		self.listBox.place(x=self.width * 0.02, y= self.height * 0.05,
		 width= self.width - (self.width * 0.04), height = self.height - (self.height * 0.20))
		
		#Scroolbar
		vsb = ttk.Scrollbar(self, orient="vertical", command=self.listBox.yview)
		vsb.place(x=self.width - (self.width * 0.02), y= self.height * 0.09, height= self.height - (self.height * 0.25))
		
		vsb2 = ttk.Scrollbar(self, orient="horizontal", command=self.listBox.xview)
		vsb2.place(x=self.width * 0.02, y= self.height - (self.height * 0.15), width= self.width - (self.width * 0.04))
		
		
		self.listBox.configure(yscrollcommand=vsb.set, xscrollcommand=vsb2.set)

		
		# set column headings
		for i,col in enumerate(columns):
			self.listBox.heading(col, text=col)
		
			
			if col == "Station Location":
				self.listBox.column(str(i), width= 270)
			elif col == "SID":
				self.listBox.column(str(i), width= 80)
			elif col == "MDA_vs_Conc.(uBq/m3)":
				self.listBox.column(str(i), width= 150)
			else:
				self.listBox.column(str(i), width= 120)
			
		self.fill_values_table(columns)
#============================================================================
	def analyze_folder_autosain(self):
		self.show_label("Analyzing Autosain Reports...")
		self.after(1000, self.run_analysis)
		
	def run_analysis(self):
		run = True
		print("Analyzing reports autosain")
		if run:
			self.excel_file_name = "clean.xlsx"
			self.df = mk.start_analysis(self.excel_file_name, self.maindir)
			self.update_label("Results")
			self.table()
			run = False
			
		print("Done with the analysis")
		
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
if __name__ == '__main__':
	root = Root()
	root.mainloop()
