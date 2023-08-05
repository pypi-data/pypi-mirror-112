
import os
from Bio import SeqIO
from PHASEfilter.lib.utils.util import Utils
from PHASEfilter.lib.utils.software import Software

class Bases(object):

	DT_BASES = {'A': 'Adenine',
			'C': 'Cytosine',
			'G': 'Guanine',
			'T': 'Thymine',
			'U': 'Uracil',
			'R': 'A, G',
			'Y': 'C, T',
			'S': 'G, C',
			'W': 'A, T',
			'K': 'G, T',
			'M': 'A, C',
			'B': 'C, G, T',
			'D': 'A, G, T',
			'H': 'A, C, T',
			'V': 'A, C, G',
			'N': 'any base'}
	
	VECT_ORDER_BASES = ['A', 'C', 'G', 'T', 'U', 'R', 'Y', 'S', 'W',\
			'K', 'M', 'B', 'D', 'H', 'V', 'N']
	
	def __init__(self):
		self.dt_count_bases = {}

	def count_bases(self, sequence):
		"""
		cout bases
		"""
		sequence_ = sequence.upper()
		for base in Bases.DT_BASES:
			self.dt_count_bases[base] = sequence_.count(base)
		
	def get_header(self):
		return "\t".join(Bases.VECT_ORDER_BASES)
	
	def __add__(self, other):
		for base in Bases.VECT_ORDER_BASES:
			if base in self.dt_count_bases: self.dt_count_bases[base] += other.dt_count_bases[base]
			else: self.dt_count_bases[base] = other.dt_count_bases[base]
		return self
	
	def __str__(self):
		return "\t".join([str(self.dt_count_bases[base]) for base in Bases.VECT_ORDER_BASES])
	
class Reference(object):

	software = Software()
	utils = Utils()
	BIGGEST_CHR = 'biggest chr'

	def __init__(self, reference_file = None):
		self.reference_dict = {}
		self.reference_length = { Reference.BIGGEST_CHR : 0 }
		self.reference_count_bases = {}
		self.vect_reference = []
		self.total_length = 0
		
		## tmp file with unzip file, if source file is zipped
		self.temp_file_name = None
		self.fasta_index_created = False
		
		## reference file
		if (not reference_file is None):
			self.reference_file = reference_file
			self.read_reference_fasta(reference_file)
			self.test_index_fasta_file()

	def __del__(self):
		"""
		remove tmp file
		"""
		if not self.temp_file_name is None and self.temp_file_name.startswith(Utils.TEMP_DIR) \
			and os.path.exists(self.temp_file_name):
			os.remove(self.temp_file_name)
		if (self.fasta_index_created and not self.temp_file_name is None):
			self.utils.remove_file(self.temp_file_name + ".fai")
		
		## close this handle
		if (len(self.reference_dict) > 0):
			self.reference_dict.close()
			

	def read_reference_fasta(self, reference_file):
		"""
		test if the reference_file and get the handle
		"""
		if (not os.path.exists(reference_file)): raise Exception("Can't locate the reference file: '" + reference_file + "'")

		if self.utils.is_gzip(reference_file):
			## create tmp file
			self.temp_file_name = self.utils.get_temp_file(os.path.basename(reference_file), ".fasta")
			cmd = "gzip -cd " + reference_file + " > " + self.temp_file_name
			os.system(cmd)
		else: self.temp_file_name = reference_file

		self.reference_dict = SeqIO.index(self.temp_file_name, 'fasta')
		for key in self.reference_dict:
			self.vect_reference.append(key)
			self.reference_length[key] = len(str(self.reference_dict[key].seq))
			self.total_length += self.reference_length[key]
			if (self.reference_length[key] > self.reference_length[Reference.BIGGEST_CHR]):
				self.reference_length[Reference.BIGGEST_CHR] = self.reference_length[key]

	def get_reference_name(self):
		"""
		:out  reference name
		"""
		return self.utils.get_file_name_without_extension(self.reference_file)

	def get_chr_length(self, chr_name):
		if (not chr_name in self.reference_length): return self.reference_length[chr_name.lower()] 
		return self.reference_length[chr_name]

	def genome_length(self):
		return self.total_length


	def get_first_seq(self):
		"""
		:param return one key
		"""
		for key in self.reference_dict: return key


	def chr_not_included(self, vect_chr_to_test):
		"""
		:out chromosomes names that not included in the input vector 
		"""
		vect_return = []
		for name in self.vect_reference:
			if (not name in vect_chr_to_test): vect_return.append(name)
		return vect_return


	def get_chr_in_genome(self, chr_name_test):
		"""
		:param chr_name_test chromosome name to get homologous in this reference
		:out name of the homologous in this reference
		"""
		dt_candidate = {}
		diff_min = 999
		for chr_name in self.vect_reference:
			(diff, equal) = (0, 0)
			for i in range(max(len(chr_name_test), len(chr_name))):
				if (i >= len(chr_name) or i >= len(chr_name_test)): diff += 1
				elif(chr_name[i].lower() != chr_name_test[i].lower()): diff += 1
				else: equal +=1
			
			total_sum = diff - equal	## more equla, more negative
			if (total_sum in dt_candidate): dt_candidate[total_sum].append(chr_name)
			else: dt_candidate[total_sum] = [chr_name]
			if (total_sum < diff_min): diff_min = total_sum 
				
		if (len(dt_candidate[diff_min]) == 1): return dt_candidate[diff_min][0]
		if (len(dt_candidate) == 0): raise Exception("Error: there isn't chr names in this reference")
		message_error = "Error: there are more than one candidate for this chr '{}' -> ['{}']\n".format(chr_name_test, "', '".join(dt_candidate[diff_min]))
		message_error += "You can not process this chr '{}' passing the follow paramateres in CLI '--pass_ref {}'".format(chr_name_test, chr_name_test)
		raise Exception(message_error)


	def test_index_fasta_file(self):
		"""
		test and create index
		"""
		index_file = os.path.join(self.temp_file_name + ".fai")
		if (not os.path.exists(index_file)):
			self.fasta_index_created = True
			cmd = "{} faidx {}".format(self.software.get_samtools(), self.temp_file_name)
			exist_status = os.system(cmd)
			if (exist_status != 0):
				raise Exception("Fail to run samtools\nCmd: {}".format(cmd))
		
	def get_base_in_position(self, chromosome, position_from, position_to, temp_file):
		"""
		:param position to return
		:out return base in this position
		"""
		cmd = "{} faidx {} {}:{}-{} > {}".format(self.software.get_samtools(), self.temp_file_name, chromosome, position_from, position_to, temp_file)
		exist_status = os.system(cmd)
		if (exist_status != 0):
			raise Exception("Fail to run samtools")
		
		vect_out_put = self.utils.read_text_file(temp_file)
		seq_to_return = ""
		if (len(vect_out_put) > 1): seq_to_return = "".join(vect_out_put[1:])
		if (len(seq_to_return) == (position_to - position_from + 1)): return seq_to_return
		if (len(vect_out_put) == 0): return ""
		raise Exception("Error: more information than expected for this position '{}:{}-{}' : {}".format(\
			chromosome, position_from, position_to, ", ".join(vect_out_put)))

	def count_bases(self):
		"""
		count bases in all chromosomes
		"""
		for chr_name in self.vect_reference:
			bases = Bases()
			bases.count_bases(str(self.reference_dict[chr_name].seq))
			self.reference_count_bases[chr_name] = bases
		print("Number of chromosomes processed: {}".format(len(self.vect_reference)))

	def save_count_bases_in_file(self, file_name):
		""" Save base statistics in a file """
		with open(file_name, 'w') as handle_write:
			bases = Bases()
			total_length = 0
			handle_write.write("Has the total number of bases per chromosome\nCromosome\tLength\t{}\n".format(bases.get_header()))
			for chr_name in self.vect_reference:
				handle_write.write("{}\t{}\t{}\n".format(chr_name, self.reference_length[chr_name], str(self.reference_count_bases[chr_name]) ))
				total_length += int(self.reference_length[chr_name])
				bases += self.reference_count_bases[chr_name]
			handle_write.write("Total\t{}\t{}\n".format(total_length, str(bases) ))
			
			### save bases:
			handle_write.write("\nBase description\n")
			bases = Bases()
			for base in bases.VECT_ORDER_BASES:
				handle_write.write("{}\t{}\n".format(base, "\t".join(bases.DT_BASES[base].split(','))))

