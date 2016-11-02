import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os


def pos(id):
	'''Convert an id number into (x,y) coordinates. Will be used in the Small_cell class to locate the small cell on the full size cell.
	The code is ulgy but there are too many specific cases to find a general expression.'''
	x=0
	y=0

	if 1 <= id <= 10:
		x = 0
		y = id + 1

	elif 11 <= id <= 22:
		x = 1
		y = id - 10

	elif 23 <= id <= 162:
		x = (id - 23) / 14 + 2
		y = (id - 23) - ((x-2) * 14)

	elif 163 <= id <= 174:
		x = 12
		y = id - 162

	elif 175 <= id <= 184:
		x = 13
		y = id - 173

	else:
		raise IndexError("The ID of the cell should be between 1 and 184.")

	return (x,y)



class Small_cell:
	'''This class contains the main solar cell parameters extracted from the IV data, 
	namely open circuit voltage (Voc), short circuit current (Isc), fill factor (FF) and efficiency (Eta). 
	The position of the solar cell given by the data parser is  added as an attribute'''

	def __init__(self,file_name):
		
		self.file_name = file_name

		''' Data parser _ Extract IV data from a csv file and returns a DataFrame containing the extracted data.
		Also extracts the position of the cell from the file name'''
		#print file
		file_handle = open(self.file_name,'r')
	
		full_data = pd.read_csv(file_handle, sep = ';', header = 1, decimal = ',')

		#Select only the voltage and current columns
		self.IV = full_data[['Voltage Measured (V)','Current Measured (A)']]

		
		file_handle.close()

		'''The file names are supposed to have the format "cell_ID.csv". The cell ID is extracted because it allows to locate the small cell 
		on the full size cell. This cell ID is converted into a tuple with (x,y) coordinates using the "pos" function defined above
		 for easy plotting in the next steps.'''

		#Considering the assumed format of the file name, the cell ID is extracted
		self.cell_ID = int(self.file_name[:-4])

		#Convert id into coordinates using the function defined above
		self.coord = pos(self.cell_ID)

		#Contain volatge data only.
		self.V = self.IV['Voltage Measured (V)']

		#Contain current data only. The '-' sign is added for convention purposes.
		self.I = -self.IV['Current Measured (A)']

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

		#The fitting equation is in the form y = ax+b. In this case y is the current (I) and x is the voltage (V). 
		#Voc is the voltage when the current is 0 => Voc = -b/a
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

		#Linear fit of I(V) around V=0 to extract Isc. 
		fit_param2 = np.polyfit(V_for_fit2, I_for_fit2,1)

		#Similar to Voc calculation but this time, the voltage is zero => Isc = b
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
		

	def Eta(self,area):
		'''Calculate the efficiency in % from IV data. Eta (efficiency) is the ratio between
		 the max power output of the cell and the normalized incident light power which is 0.1 W/cm2. The area of the cell 
		 in cm2 must be given to calculate efficiency. The standard is 1cm2.'''

		return 100 * self.pmax / (0.1*area)


	
class Full_size_cell:
	''' Extract the solar cell parameters of all 184 small cells in a full size cell. The data is stored in 184 .csv files
	which names are written according to the following format : 'cell_ID.csv' to locate the small cells on the full size cell. All the
	files are in the same folder called "input_path"'''

	def __init__(self, input_path):
		self.input_path = input_path
		

		list_of_files = os.listdir(self.input_path)
		

		#Initialization of the list that will contain a Small_cell object for each file in the directory
		self.small_cells = []

		#go to the directory for data extraction
		os.chdir(self.input_path)
		

		# list of possible names for files in the folder		
		check = [str(n)+'.csv' for n in range(185)]

		# check if the folder only contains file that can be treated by the program
		for i in list_of_files:
			if i not in check:
				raise TypeError('Not all the files in the specified directory are compatible with this program. The file format should be "cell_ID.csv"')

		"""create a list of small cells containing data extracted from each csv file in the folder. 
		The full size cell is not square (it has rounded corners) so coordinates such as (0,0) or (0,1) do not correspond to any small cell."""
		self.small_cells = [Small_cell(f) for f in list_of_files]
		#print self.small_cells

		# rearrange the list of small cells in a dictionnary where the keys are the coordinates
		self.small_cells_dic = {self.small_cells[i].coord : self.small_cells[i] for i in range(len(self.small_cells))}

		# generate the maps of parameters. If a measurement file for a small cell does not exists, the corresponding parameters are set to 0.
		self.Voc_map = np.asarray([[self.small_cells_dic[(i,j)].Voc() if (i,j) in self.small_cells_dic.keys() else 0 for i in range(15)] for j in range(15) ])
		self.Isc_map = np.asarray([[self.small_cells_dic[(i,j)].Isc() if (i,j) in self.small_cells_dic.keys() else 0 for i in range(15)] for j in range(15) ])
		self.FF_map = np.asarray([[self.small_cells_dic[(i,j)].FF() if (i,j) in self.small_cells_dic.keys() else 0 for i in range(15)] for j in range(15) ])
		self.Eta_map = np.asarray([[self.small_cells_dic[(i,j)].Eta(1) if (i,j) in self.small_cells_dic.keys() else 0 for i in range(15)] for j in range(15) ])

	
	def plot_Voc_map(self):	

		'''Plot a map representing the distribution of the open circuit voltage. Will be used in the Full_size_cell class.'''

		# generate 2 2d grids for the x & y bounds
		x, y = np.mgrid[slice(0, 15, 1), slice(0, 15, 1)]

		#Create two figures to compare two methods. First pcolormesh is tried and then contourf.The contourf was chosen eventually.
		

		'''#pcolormesh
		plt.figure(1)
		im = plt.pcolormesh(x, y, self.Voc_map)
		c1 = plt.colorbar(im)
		c1.ax.set_ylabel('Voc [V]')
		plt.title('Open circuit voltage distribution (1)')
		plt.xlabel('y coordinate')
		plt.ylabel('x coordinate')
		plt.gca().set_aspect('equal')'''
		
		#contourfs
		#arrange the color scale
		step = 0.01
		levels = np.arange(self.Voc_map.min(),self.Voc_map.max()+step,step)

		# contours are *point* based plots, so convert our bound into point
		# centers
		cf = plt.contourf(x[:-1, :-1], y[:-1, :-1], self.Voc_map[:-1, :-1], levels)
		c2 = plt.colorbar(cf)
		c2.ax.set_ylabel('Voc [V]')
		plt.title('Open circuit voltage')
		plt.xlabel('y coordinate')
		plt.ylabel('x coordinate')
		plt.gca().set_aspect('equal')


		

	def plot_Isc_map(self):
		'''Plot a map representing the distribution of the short circuit current. Will be used in the Full_size_cell class.'''

		# generate 2 2d grids for the x & y bounds
		x, y = np.mgrid[slice(0, 15, 1), slice(0, 15, 1)]

		#Create two figures to compare two methods. First pcolormesh is tried and then contourf.The contourf was chosen eventually.
		

		'''#pcolormesh
		plt.figure(1)
		im = plt.pcolormesh(x, y, self.Isc_map)
		c1 = plt.colorbar(im)
		c1.ax.set_ylabel('Isc [A]')
		plt.title('Short circuit current distribution (1)')
		plt.xlabel('y coordinate')
		plt.ylabel('x coordinate')
		plt.gca().set_aspect('equal')'''
		
		#contourfs
		#arrange the color scale
		
		step = 0.001
		levels = np.arange(self.Isc_map.min(),self.Isc_map.max()+step,step)

		# contours are *point* based plots, so convert our bound into point
		# centers
		cf = plt.contourf(x[:-1, :-1], y[:-1, :-1], self.Isc_map[:-1, :-1], levels)
		c2 = plt.colorbar(cf)
		c2.ax.set_ylabel('Isc [A]')
		plt.title('Short circuit current')
		plt.xlabel('y coordinate')
		plt.ylabel('x coordinate')
		plt.gca().set_aspect('equal')


		

	def plot_FF_map(self):
		'''Plot a map representing the distribution of the fill factor. Will be used in the Full_size_cell class.'''

		# generate 2 2d grids for the x & y bounds
		x, y = np.mgrid[slice(0, 15, 1), slice(0, 15, 1)]

		#Create two figures to compare two methods. First pcolormesh is tried and then contourf. The contourf was chosen eventually.
		

		'''#pcolormesh
		plt.figure(1)
		im = plt.pcolormesh(x, y, self.FF_map)
		c1 = plt.colorbar(im)
		c1.ax.set_ylabel('FF [%]')
		plt.title('Fill factor distribution (1)')
		plt.xlabel('y coordinate')
		plt.ylabel('x coordinate')
		plt.gca().set_aspect('equal')'''
		
		#contourfs
		#arrange the color scale
		
		step = 1
		levels = np.arange(self.FF_map.min(),self.FF_map.max()+step,step)

		# contours are *point* based plots, so convert our bound into point
		# centers
		cf = plt.contourf(x[:-1, :-1], y[:-1, :-1], self.FF_map[:-1, :-1], levels)
		c2 = plt.colorbar(cf)
		c2.ax.set_ylabel('FF [%]')
		plt.title('Fill factor')
		plt.xlabel('y coordinate')
		plt.ylabel('x coordinate')
		plt.gca().set_aspect('equal')


		

	def plot_Eta_map(self):
		'''Plot a map representing the distribution of the efficiency. Will be used in the Full_size_cell class.'''

		# generate 2 2d grids for the x & y bounds
		x, y = np.mgrid[slice(0, 15, 1), slice(0, 15, 1)]

		#Create two figures to compare two methods. First pcolormesh is tried and then contourf. The contourf was chosen eventually.
		

		'''#pcolormesh
		plt.figure(1)
		im = plt.pcolormesh(x, y, self.Eta_map)
		c1 = plt.colorbar(im)
		c1.ax.set_ylabel('Efficiency [%]')
		plt.title('Efficiency distribution (1)')
		plt.xlabel('y coordinate')
		plt.ylabel('x coordinate')
		plt.gca().set_aspect('equal')'''
		
		#contourfs
		#arrange the color scale
		
		step = 0.2
		levels = np.arange(self.Eta_map.min(),self.Eta_map.max()+step,step)

		# contours are *point* based plots, so convert our bound into point
		# centers
		cf = plt.contourf(x[:-1, :-1], y[:-1, :-1], self.Eta_map[:-1, :-1], levels)
		c2 = plt.colorbar(cf)
		c2.ax.set_ylabel('Efficiency [%]')
		plt.title('Efficiency')
		plt.xlabel('y coordinate')
		plt.ylabel('x coordinate')
		plt.gca().set_aspect('equal')


		
	

	def sum_plot(self):
		'''Plot the distribution of all four parameters using contouf function'''

		plt.figure()

		plt.subplot(221)
		self.plot_Voc_map()

		plt.subplot(222)
		self.plot_Isc_map()

		plt.subplot(223)
		self.plot_FF_map()

		plt.subplot(224)
		self.plot_Eta_map()

		plt.show()







#Test _  A testing folder for this program is available under python_homework\Project\uniformity_U1140712\raw
F1 = Full_size_cell('C:\Users\Patrice.Bras\Github\python_homework\Project\uniformity_U1140712\\raw')

#Test _ see if sum_plot has the expected output 
F1.plot_Voc_map()

F1.sum_plot()

#Go back to the project directory
os.chdir('C:\Users\Patrice.Bras\Github\python_homework\Project')











