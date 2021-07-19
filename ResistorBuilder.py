# This is to make a resistor circuit of certian depth and resistance
# Written By Trevor Craig
# Started on July 16 2021

# Theory take a know resistance and number of resistors
# Build a value as close as possible to that number
# Start with a series connection and then go parrell
# Go severeral layers to get as close as possible

import csv
import sys

# Made  Class To be able to import later
class ResistorSelector:
	def __init__(self, filename,WantedResistance,NumberOfLayers=10):
		self.filename=filename
		self.WantedResistance=WantedResistance
		self.UpdatedResistorList=[]
		self.UsedResistors=[]
		self.ReadInCSV()
		self.ResistanceTotal=0
		self.Layers=[]
		LayerCount=0
		while(self.AddLayer(self.WantedResistance-self.ResistanceTotal)):
			LayerCount=LayerCount+1
			if(LayerCount==NumberOfLayers):
				break
							
		self.PrintLayers()
		
	# This function just prints the specific layers for series and parrell		
	def PrintLayers(self):
		print("Goal of "+str(self.WantedResistance))
		print("Equivalent Circuit Resistance of "+ str(self.ResistanceTotal))
		for IndLayer in self.Layers:
			printstring=str(IndLayer.LayerType)
			for value in IndLayer.UsedResistors:
				printstring=printstring+" "+str(value)+ " "
			print(printstring)
			
	# This function attempts to add another layer for series or parrell	
	def AddLayer(self,resistance):
		LayerOption=self.Layer(resistance,self.UpdatedResistorList)
		if(len(LayerOption.UsedResistors)<1):
			return(0)
		for value in LayerOption.UsedResistors:
			self.UpdatedResistorList.remove(value)
			self.UsedResistors.append(value)
		self.ResistanceTotal=self.ResistanceTotal+LayerOption.EquivalentResistance
		self.Layers.append(LayerOption)
		return(1)
	
	# Just reading in the CSV File
	# Could add check to see if file exists
	# Also could add the tolerances on the resistors
	# Might want the watt ratings as well	
	def ReadInCSV(self):
		with open(self.filename, newline='') as csvfile:
			reader = csv.reader(csvfile, delimiter=',', quotechar='|')
			for row in reader:
				self.AddResistortoList(float(row[0]),int(row[1]))
				
	# Helper funtion just to add resistors to the list			
	def AddResistortoList(self,value,quanity):
		for i in range(0,quanity): 
			self.UpdatedResistorList.append(value)
			
	# This is the layer that decideds what type it is	
	class Layer:
		def __init__(self,RequiredResistance,UpdatedResistorList):
			self.UsedResistors=[]
			self.UpdatedResistorList=UpdatedResistorList
			self.RequiredResistance=RequiredResistance
			#print(RequiredResistance)
			self.LayerType=""
			self.EquivalentResistance=0
			FoundResistor=self.CheckForClosestValue()
		
			if (FoundResistor == 0):
				ReutrnedResistors=self.BuildAParrel()
				if len(ReutrnedResistors)>0:
					for value in ReutrnedResistors:
						self.UsedResistors.append(value)
				
					self.LayerType="Parallel"
					self.EquivalentResistance=self.EquivalentResistanceParrell(ReutrnedResistors)
					#print(ReutrnedResistors)
				else:
					self.LayerType="NONE"
					self.EquivalentResistance=0
			else:
				self.UsedResistors.append(FoundResistor)
				self.LayerType="Series"
				self.EquivalentResistance=FoundResistor
				#print(FoundResistor)
			
		def CheckForClosestValue(self):
			FoundResistor=0
			for value in self.UpdatedResistorList:
				DifferanceInResistance=self.RequiredResistance-value
				if (DifferanceInResistance>0):
					if (FoundResistor == 0):
						LowestDiffernce=DifferanceInResistance
						FoundResistor=value
					else:
						if(LowestDiffernce>DifferanceInResistance):
							FoundResistor=value
							LowestDiffernce=DifferanceInResistance
			return(FoundResistor)
			
		def BuildAParrel(self):
			WorkingList=self.UpdatedResistorList.copy()
			FoundResistors=[]
			NumberofResistors=2 #Start with two resistors
			while (NumberofResistors<len(self.UpdatedResistorList.copy())):
				WorkingList=self.UpdatedResistorList.copy()
				while len(WorkingList)>NumberofResistors:
					ArrayOfSmalls=self.ParellCircuitNum(NumberofResistors,WorkingList)
					self.RemoveItemsFromList(ArrayOfSmalls, WorkingList)
					ResistorOption=self.EquivalentResistanceParrell(ArrayOfSmalls)
					if(self.RequiredResistance>=ResistorOption):
						FoundResistors=ArrayOfSmalls
						return(FoundResistors)
					else:
						# Values didn't work remove one value and try again 
						for count, value in enumerate(ArrayOfSmalls):
							if count == 0:
								pass
							else:
								WorkingList.append(value)
								
				NumberofResistors=NumberofResistors+1
			return(FoundResistors)
				
		def RemoveItemsFromList(self,RemoveList, WorkingList):
			for item in RemoveList:
				WorkingList.remove(item)
					
		def ParellCircuitNum(self,Number,ListofValues):
			ArrayOfSmalls=[]
			ListofValuesToChange=ListofValues.copy()
			for i in range(0,Number):
				Temp=min(ListofValuesToChange)
				ListofValuesToChange.remove(Temp)
				ArrayOfSmalls.append(Temp)
			return(ArrayOfSmalls)
		
		def EquivalentResistanceParrell(self,ResistorList):
			EquivResist=0
			for value in ResistorList:
				EquivResist=EquivResist+1/value
			return(1/EquivResist)

def main():
	#Option to use a command line Sturcture for reading in resistance and the file
	if len(sys.argv) > 1:
		filename=str(sys.argv[1])
		WantedResistance=float(sys.argv[2])
		NumberOfLayers=10 # How many iterations you want it to go this can be as high as you want
		ResistorList=ResistorSelector(filename,WantedResistance,NumberOfLayers)
	else:
		filename="ResistorList.csv" # Enter the list of resistors here value, quanity
		WantedResistance=655 # Enter How much resistance you want here
		NumberOfLayers=10 # How many iterations you want it to go this can be as high as you want
		ResistorList=ResistorSelector(filename,WantedResistance,NumberOfLayers)


if __name__ == "__main__":
	print("Starting")
	main()
	print("Finishing")
