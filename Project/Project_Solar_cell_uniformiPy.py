import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from os import listdir

def IV_data_parser(file):
	''' Extract IV data from a csv file and returns a DataFrame containing the extracted data'''

	file_handle = open(file,'r')
	
	full_data = pd.read_csv(file_handle, sep = ';', header = 1, decimal = ',')

	#Select only the voltage and current columns
	IV_data = full_data[['Voltage Measured (V)','Current Measured (A)']]

	#print full_data.keys()
	file_handle.close()

	#print IV_data
	return IV_data
	

class Small_cells:
	'''This class contains the main solar cell parameters extracted from the IV data, 
	namely open circuit voltage (Voc), short circuit current (Isc), fill factor (FF) and efficiency (Eta)'''

	def __init__(self,IV):
		self.IV = IV

		#Contain volatge data only.
		self.V = IV['Voltage Measured (V)']

		#Contain current data only. The '-' sign is added for convention purposes.
		self.I = -IV['Current Measured (A)']

		#Power is definined as voltage multiplied by current
		self.P = self.V * self.I
		

		#The maximum power output of the solar cell is an interesting parameter to have access to (for FF and efficiency calculation for instance)
		self.pmax = max(self.P)


	def Voc(self):
		'''Calculate the open circuit volatge from IV data. Voc is defined as the voltage when the current
		is equal to 0.'''

		#range of the fit for Voc calculation  
		fit_range = 4

		#Extract 4 elements of the V and I columns for indexes where I is around 0
		for i in range(len(self.I)):
			if self.I[i] > 0 and self.I[i+1] <= 0:
				V_for_fit1 = [x for x in self.V[i-(fit_range/2)+1 : i+(fit_range/2)+1]]
				I_for_fit1 = [y for y in self.I[i-(fit_range/2)+1 : i+(fit_range/2)+1]]

		#Linear fit of I(V) around I=0 to extract Voc
		fit_param1 = np.polyfit(V_for_fit1, I_for_fit1,1)

		return -fit_param1[1]/fit_param1[0]

	def Isc(self):
		'''Calculate the short circuit current from IV data. Isc is defined as the current when the voltage is equal to 0.'''

		#range of the fit for Isc calculation
		fit_range = 4

		#Extract 4 elements of the V and I columns for indexes where V is around 0
		for v in range(len(self.V)):
			if self.V[v] <= 0 and self.V[v+1] >0:
				V_for_fit2 = [x for x in self.V[v-(fit_range/2)+1 : v+(fit_range/2)+1]]
				I_for_fit2 = [y for y in self.I[v-(fit_range/2)+1 : v+(fit_range/2)+1]]

		#Linear fit of I(V) around V=0 to extract Isc
		fit_param2 = np.polyfit(V_for_fit2, I_for_fit2,1)

		return fit_param2[1]


	def FF(self):
		'''Calculate the fill factor from IV data. FF is defined as the ratio between the product of Isc and Voc,
		and the product of the voltage and current when the power is at maximum'''

		#Index of the maximum power
		
		i_pmax = self.P.idxmax()

		#Voltage and current at maximum power
		V_pmax = self.V[i_pmax]
		I_pmax = self.I[i_pmax]

		#Return FF in %
		return 100 * (V_pmax*I_pmax) / (self.Voc()*self.Isc())
		

	def Eta(self):
		'''Calculate the efficiency in % from IV data. Eta (efficiency) is the ratio between
		 the max power output of the cell and the normalized incident light power which is 0.1 W/cm2'''

		return 100 * self.pmax / 0.1


	
class Full_size_cell:
	''' Extract the solar cell parameters of all 184 small cells in a big cells. The data is stored in 184 .csv files
	which names are written according to the following format to locate the small cells on the full size cell. All the
	files are in the same folder called "dir"'''

	def __init__(self, input_path)


S1 = Small_cells(IV1)

print S1.Voc()
print S1.Isc()
print S1.FF()
print S1.Eta()





