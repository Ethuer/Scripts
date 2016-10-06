#import re
import xlrd
import numpy as np
import csv
#import matplotlib.pyplot as plt
from Tkinter import *

from tkinter import *
from tkinter import ttk
from tkFileDialog import askopenfilename

from tkinter.messagebox import showerror

class MyFrame(Frame):
	
	def increaseOrientation(self,orient):
		if orient[0] <= 10:
			orient[0] +=1
		if orient[0] > 10:
			orient[0] = 3
			orient[1] +=1
			
		return orient
	
	
	def __init__(self):
		Frame.__init__(self)
		self.master.title("Plate Parser 0.1")
		self.master.rowconfigure(0, weight=2)
		self.master.columnconfigure(0, weight=2)
		self.grid() #sticky=W+E+N+S)
		self.v = StringVar()
		self.checkDict = {}
		
		letters = ['A','B','C','D','E','F','G','H']
		
		self.Letter2row = {}
		startOfRows = 11
		for letter in letters:
			self.Letter2row[letter] = startOfRows
			startOfRows+=1
		
		for element in letters:
			for f in [1,4,7,10]:
				var = '%s%i' %(element,f)
				el = IntVar()
				self.checkDict[var] = Checkbutton(variable = el, text=str(var))
				self.checkDict[var].var = el
			
		orientation = [3,1] # startposition
		for f in [1,4,7,10]:
			for element in letters:
			
				var = '%s%i' %(element,f)
				self.checkDict[var].grid(row=orientation[0],column =orientation[1],sticky=E)
				orientation = self.increaseOrientation(orientation)
								
		

		self.explanation = Label(self, text="Choose file")
		self.explanationOut = Label(self, text="Enter outfile name")
		self.chosenFile = Label(self,text=self.v)
		self.entry = Entry(self,textvariable = '')
		self.entryOutFile = Entry(self,textvariable = '')
		self.button = Button(self, text="Browse", command=self.load_file, width=10)
		self.start = Button(self, text="Start",command=self.startParsing, width=10) #  command=self.load_file,

		
		self.explanation.grid(row=1,column=0 )
		self.explanationOut.grid(row=2,column=0 )
		self.entry.grid(row=1,column=2)
		self.entryOutFile.grid(row=2,column=2)
		self.button.grid(row=1, column=4)
		self.start.grid(row= 2, column = 5)


	

	def startParsing(self):
		print self.entry.get()
		book = xlrd.open_workbook('%s' %(self.entry.get()))
		
		layout = book.sheet_by_index(0)
		
		conditionList = []
		self.choiceToObjects(layout)

		#~ print book.nsheets
		for sheet in range(1,book.nsheets):
		
			current = book.sheet_by_index(sheet)
			conditionList.append(current.name)

			for obs in self.obsList:
				obs.addSheet(current)
				
		#~ print len(self.obsList), len(conditionList)
			
		with open('%s'%(self.entryOutFile.get()),'w') as outhandle:
			outfile = csv.writer(outhandle, delimiter = '\t')
		
			outRow = []
			outRow.append('ID')
			for element in conditionList:
				outRow.append(element)
			outfile.writerow(outRow)
			
			for obs in self.obsList:
				outRow = []
				try:
					outRow.append(obs.name.encode('utf-8'))
				except:
					outRow.append(obs.name) 
					print obs.name
				for key, element in obs.observationDict.items():
					outRow.append("%.2f" %(element))
				
				outfile.writerow(outRow)
				
			
			#~ for element in 
			


			
		
		
		
	
	def choiceToObjects(self, layout):
		self.obsList = []
		for key, value in self.checkDict.items():
			if value.var.get() == 1:
				# new baseLine,  find rows and such
				row,cols = self.findPosition(key)
				label = self.findlabel(layout,row,cols,key)
				obs = observation(label,row,cols)
				self.obsList.append(obs)
			
			
	
	
		
	def findPosition(self,LetterNumber):
		Number = LetterNumber[1:]
		Letter = LetterNumber[0]
		row = self.Letter2row[Letter]
		columns = [int(Number),int(Number)+1,int(Number)+2]
		return row,columns
		
		
	def findlabel(self,layout,row,cols,index):
		label = index
		try:
			for col in cols:
				lab = layout.cell(row, col).value
				if lab != '':
					label = lab
					print lab
		except:
			pass # not essential function, no need to catch
			
		return label
	
		
	def showname(self):
		name = '%s' %(self.bookname)
		#self.entry.insert(master, name)
		

	def load_file(self):
		self.bookname = askopenfilename()
		if self.bookname:
			#~ print("file selected " , self.bookname)
			self.entry.insert(0,self.bookname)
			

		



def readTable(sheet, sheetDict):
       outDict = {}

       totList = []
       label = sheet.label
       for row in range(11,18):
              rowList = []
              for col in range(1,13):
                     rowList.append(sheet.cell(row,col))
              totList.append(rowList)
       sheetDict[sheet.label] = totList
       return


class observation():
	def __init__(self, name,row, columns):
              self.observationDict = {}
              self.stdevDict = {}
              self.row = row
              self.columns = columns
              self.name = name
              

	def addobservation(self,label,tableDict):
              row = self.row
              listing = [obs1,obs2,obs3]
              self.observationDict[label]= np.mean(listing)
              self.stdevDict[label]= np.std(listing)

	def addSheet(self,sheet):
			row = self.row
			listing = []
			for col in self.columns:
				try:
					arg = sheet.cell(int(row),int(col))
					listing.append(float(str(arg).split(':')[1]))
				except:
					print "failed to convert " , sheet.cell(row,col)
					print   row, col
				

			self.observationDict[sheet.name] = np.mean(listing)
			self.stdevDict[sheet.name] = np.std(listing)

              


if __name__ == "__main__":
    MyFrame().mainloop()

# manually create layout:

#1	2	3	4	5	6	7	8	9	10	11	12

#observation categorization


#~ 
#~ 
#~ cpLNCrna11 = observation('cpLNCrna11',11,[1,2,3]) 
#~ cpLNCrna21 = observation('cpLNCrna21',11,[4,5,6]) 
#~ cpLNCrna11NAT = observation('cpLNCrna11NAT',11,[7,8,9])
#~ cpLNCrna21NAT = observation('cpLNCrna21NAT',11,[10,11,12]) 
#~ 
#~ cpLNCrna11ORF = observation('cpLNCrna11ORF',12,[1,2,3]) 
#~ cpLNCrna21ORF = observation('cpLNCrna21ORF',12,[4,5,6]) 
#~ cpLNCrna11ORFNAT = observation('cpLNCrna11ORFNAT',12,[7,8,9]) 
#~ cpLNCrna21ORFNAT = observation('cpLNCrna21ORFNAT',12,[10,11,12]) 
#~ 
#~ cpLNCrna11FS = observation('cpLNCrna11FS',13,[1,2,3]) 
#~ cpLNCrna21FS = observation('cpLNCrna21FS',13,[4,5,6]) 
#~ cpLNCrna11NATFS = observation('cpLNCrna11NATFS',13,[7,8,9]) 
#~ cpLNCrna21NATFS = observation('cpLNCrna21NATFS',13,[10,11,12]) 
#~ 
#~ cpLNCrna11RC = observation('cpLNCrna11RC',14,[1,2,3]) 
#~ cpLNCrna21RC = observation('cpLNCrna21RC',14,[4,5,6]) 
#~ cpLNCrna11NATRC = observation('cpLNCrna11NATRC',14,[7,8,9]) 
#~ cpLNCrna21NATRC = observation('cpLNCrna21NATRC',14,[10,11,12]) 
#~ 
#~ cpLNCrna21empty = observation('cpLNCrna21empty',15,[4,5,6]) 
#~ cpLNCrna21emptyNAT = observation('cpLNCrna21NATempty',15,[7,8,9]) 
#~ 
#~ cpLNCrna21CLIB = observation('cpLNCrna21CLIB',16,[4,5,6]) 
#~ cpLNCrna21CLIBNAT = observation('cpLNCrna21CLIBNAT',16,[7,8,9])
#~ 
#~ cpLNCrna21CLIBRI = observation('cpLNCrna21CLIBRI',17,[4,5,6]) 
#~ cpLNCrna21CLIBRINAT = observation('cpLNCrna21CLIBRINAT',17,[7,8,9])
#~ 
#~ cpLNCrna21neg = observation('cpLNCrna21neg',18,[4,5,6]) 
#~ cpLNCrna21negNATF = observation('cpLNCrna21NAT',18,[7,8,9]) 
#~ 
#~ 
#~ allList = []
#~ 
#~ allList.append(cpLNCrna11) 
#~ allList.append(cpLNCrna21)
#~ allList.append(cpLNCrna11NAT) 
#~ allList.append(cpLNCrna21NAT)
#~ allList.append(cpLNCrna11ORF) 
#~ allList.append(cpLNCrna21ORF) 
#~ allList.append(cpLNCrna11ORFNAT) 
#~ allList.append(cpLNCrna21ORFNAT) 
#~ allList.append(cpLNCrna11FS) 
#~ allList.append(cpLNCrna21FS) 
#~ allList.append(cpLNCrna11NATFS) 
#~ allList.append(cpLNCrna21NATFS) 
#~ allList.append(cpLNCrna11RC) 
#~ allList.append(cpLNCrna21RC) 
#~ allList.append(cpLNCrna11NATRC) 
#~ allList.append(cpLNCrna21NATRC ) 
#~ allList.append(cpLNCrna21empty) 
#~ allList.append(cpLNCrna21emptyNAT) 
#~ allList.append(cpLNCrna21CLIB) 
#~ allList.append(cpLNCrna21CLIBNAT) 
#~ allList.append(cpLNCrna21CLIBRI) 
#~ allList.append(cpLNCrna21CLIBRINAT) 
#~ allList.append(cpLNCrna21neg) 
#~ allList.append(cpLNCrna21negNATF)


#~ 
#~ with open('sheetout.tsv','w') as out_raw:
	#~ outfile = csv.writer(out_raw, delimiter = '\t')
#~ 
	#~ book = xlrd.open_workbook('%s' %(bookname))
#~ 
#~ 
#~ 
	#~ layout = book.sheet_by_index(0)
#~ 
#~ 
	#~ conditionList = []
#~ 
	#~ for sheet in range(1,book.nsheets):
		#~ 
		#~ current = book.sheet_by_index(sheet)
		#~ conditionList.append(current.name)
#~ 
		#~ for obs in allList:
			#~ obs.addSheet(current)
			#~ 
#~ 
	#~ sheet =  book.sheet_by_index(6)
#~ 
	#~ outfile.writerow(conditionList)
#~ 
		#~ 
	#~ listOfInterest = ['cpLNCrna21NAT']
	#~ listOfInterest.append('cpLNCrna21NATempty')
	#~ listOfInterest.append('cpLNCrna21ORFNAT')
	#~ listOfInterest.append('cpLNCrna21NATFS')
	#~ listOfInterest.append('cpLNCrna21NATRC')	
		#~ 
	#~ 
	#~ plt.figure()
	#~ 
	#~ 
	#~ indexList = []
	#~ idx = 0
	#~ for element in conditionList:
		#~ indexList.append(idx)
		#~ idx+=1
		#~ 
	#~ 
	#~ for condition in allList:
		#~ 
		#~ if condition.name in listOfInterest:
			#~ label = condition.name
			#~ outList = []
			#~ stDevList = []
#~ 
			#~ for element in conditionList:
#~ 
				#~ outList.append(float(condition.observationDict[element]))
				#~ stDevList.append(float(condition.stdevDict[element]))
			#~ 
		#~ 
	#~ 
#~ 
			#~ print label
			#~ plt.errorbar(indexList ,outList, yerr=stDevList,  label=label)
		#~ 
			#~ plt.legend()
		#~ 
			#~ outfile.writerow(outList)
	#~ 
	#~ 
	#~ 
#~ plt.show()
#~ 
	#~ 
	#~ 
	#~ 
	
	
		#~ 
#~ y = [0.12,0.14,0.14,0.15,0.15,0.15,0.16,0.16,0.17,0.17,0.17,0.17,0.17,0.17,0.17,0.17,0.17,0.18,0.17,0.17,0.17,0.17,0.17,0.17,0.18,0.18,0.17,0.18,0.18,0.17,0.17,0.17,0.17,0.18,0.17,0.17,0.18,0.17,0.17,0.17,0.17,0.17,0.17,0.17,0.17,0.17,0.17,0.17,0.17]
#~ x = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49]
#~ yerror =[0.0122666667,0.0,0.1143333333,0.0145,0.0154333333,0.0153,0.0157333333,0.0162666667,0.017,0.0171,0.0168333333,0.0167666667,0.0165333333,0.0167,0.0166,0.0170333333,0.0171,0.0175333333,0.0171333333,0.0172666667,0.0173,0.0174,0.0174333333,0.0173333333,0.0175666667,0.0179666667,0.0174,0.0175333333,0.0178666667,0.0173666667,0.0167333333,0.0170333333,0.0170666667,0.0175,0.0173333333,0.0174,0.0177333333,0.0173666667,0.0169666667,0.0169666667,0.0169,0.0168666667,0.0166,0.0165666667,0.0165666667,0.0168333333,0.0166,0.0166333333,0.0165666667]
#~ y2 = [0.13,0.13,0.14,0.16,0.16,0.17,0.20,0.20,0.22,0.23,0.25,0.26,0.29,0.29,0.31,0.32,0.33,0.34,0.35,0.39,0.41,0.43,0.60,0.70,0.83,0.96,1.03,1.08,1.13,1.17,1.19,1.23,1.30,1.32,1.32,1.34,1.32,1.33,1.34,1.32,1.37,1.38,1.38,1.36,1.36,1.39,1.34,1.44,1.34]
#~ 
#~ 
#~ # example variable error bar values
#~ yerr = 0.1 + 0.2*np.sqrt(x)
#~ xerr = 0.1 + yerr
#~ 
#~ # First illustrate basic pyplot interface, using defaults where possible.
#~ 
#~ plt.errorbar(x, y, yerr=yerror)
#~ plt.errorbar(x, y2, yerr=yerror)
#~ plt.title("")
		
		
		
		#print len(obs.observationDict), len(obs.stdevDict)
#~ 
#~ for row in range(11,18):
       #~ for col in range(1,13):
              #~ if layout.cell(row,col) != '' and 'empty' not in str(layout.cell(row,col)):
                     #~ try:
                            #~ print row, str(layout.cell(row,col)).split('\u0394/\u0394')[1]
                     #~ except :
                            #~ print row # str(layout.cell(row,col))
#~ 


#print str(layout.cell(11,4)).split('\u0394/\u0394')[2].split("'")[0]
#print str(layout.name).split('u')[0]
#for row in range(1



#for n in range(1,book.nsheets):
#       print book.sheet_by_index(n).name
