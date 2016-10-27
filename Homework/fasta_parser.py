
import os
import matplotlib.pyplot as plt

class FastaParser(object):
	def __init__(self, path):
		self.path = path

		if not os.path.isfile(self.path):
			raise IOError("There is no file at the path specified")

		if self.path == None:
			raise TypeError("You did not specify a file path")
		
		file_in_path = open(self.path,'r') 

		#Extraction of the names of the sequences in a list seq_names assuming that it starts with '>'
		seq_names = [c.strip('>\n') for c in open(self.path) if (c.startswith('>'))]
		#print seq_names

		file_in_path.close()
		file_in_path = open(self.path,'r')


		#Extraction of the corresponding sequences in a list seq. Works also if the sequence extends on several lines.
		seq = ['']
		
		i = 0
		for s in file_in_path:	

			if s.strip('>\n') in seq_names and seq == ['']:	
				pass

			elif s.strip('>\n') in seq_names and seq != ['']:
				seq.append('')
				i += 1
				

			else:
				seq[i] = seq[i] + s.strip('\n')
					
		#print seq

		file_in_path.close()

		# The number of sequences in the file is normally equal to the length of seq.
		self.count = len(seq)
		self.seq = seq
		self.seq_names = seq_names
		#print seq_names

		#To summarize. we have 1 list seq_names containing the names of the sequences 
		#and another one seq containing the sequences themselves.
		#An intersting feature for accessing the data is to link those two lists in a dictionary Dseq

		self.Dseq = {seq_names[i] : seq[i] for i in range(self.count)}
		#print self.Dseq

		#A list conttaining the lengths of the sequences in self.seq
		self.seq_len = [len (l) for l in self.seq]
		#print self.seq_len

		#This variable is returned by the len() function applied to an instance of FastaParser
	def __len__(self):
		''' Easy access to the number of sequences'''
		return self.count

		
	def __getitem__(self,y):
		''' Modifies the getitem so that it is possible to index with a number or an ID of the list'''

		if type(y) == int:
		    if y > (len(self.seq)-1):
			    raise IndexError("This number is too high, there are not that many sequences in the file.")
		    return self.seq[y]

		elif type(y) == str:
			if y not in self.Dseq.keys() :
				raise KeyError("This is not one of the IDs of the sequences in the file.")
			return self.Dseq[y]

		else:
			raise TypeError("Sorry, no sequence is identified by what you entered...")

	def extract_length(self, max):
		''' Will filter out sequences that have more than max elements'''

		filt_seq =[l for l in self.seq if len(l) <= max]

		return filt_seq

	def length_dist(self, output):
		'''Creates a graph of the length distribution of the sequences and saves it in pdf format in the specified path'''
		
		plt.bar(range(len(self.seq)), self.seq_len, align = 'center')
		plt.xticks(range(len(self.seq_names)), self.seq_names)
		plt.xlabel('Sequence in the file')
        plt.ylabel('Length of the sequence')
        plt.title('Length distribution of the sequences')
        plt.show()
        plt.savefig(output)

		
		








