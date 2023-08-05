'''
Created on 13/11/2018

@author: mmp
'''
from Bio import SeqIO
import getpass, os, random, stat
import sys

class Utils(object):
	'''
	classdocs
	'''
	
	TEMP_DIR = os.getenv("TMP", "/tmp")

	def __init__(self, project_name = None, temp_dir = None):
		'''
		param: project_name -> used in temp diretories
		param: temp_dir -> used in temp diretories
		
		'''
		self.project_name = "generic" if project_name is None else project_name 
		self.temp_dir = Utils.TEMP_DIR if temp_dir is None else temp_dir 
	
	def is_integer(self, n_value):
		try:
			int(n_value)
			return True
		except ValueError: 
			return False
	
	def is_float(self, d_value):
		try:
			float(d_value)
			return True
		except ValueError: 
			return False
		
	def is_string(self, sz_value):
		"""
		Test if it is string
		"""
		return (not self.is_integer(sz_value) and not self.is_float(sz_value))
	

	def read_key_from_file(self, file_name, b_convert_value_to_int = False, b_aggregate_same_key = False):
		"""
		Read key file
		# ID
		sdf
		sdfs
		sgsd
		sdgsd
		
		OR
		
		Read key file
		# ID
		sdf xpto1
		sdfs zpt1
		sgsd art1
		sdgsd lrt1
		
		return  { "sdf":1, "sdfs":1, "sgsd":1, "sdgsd":1 }
		or 
		return  { "sdf":xpto1, "sdfs":zpt1, "sgsd":art1, "sdgsd":lrt1 }
		"""
		
		dict_data = {}
		if (not os.path.exists(file_name)): return dict_data
		with open(file_name) as handle_in:
			for line in handle_in:
				sz_temp = line.strip()
				if (len(sz_temp) == 0 or sz_temp[0] == '#'): continue
				lst_data = sz_temp.split()
				if (lst_data[0] in dict_data):
					if (b_aggregate_same_key): dict_data[lst_data[0]].append(0 if len(lst_data) == 1 else (int(lst_data[1]) if b_convert_value_to_int else lst_data[1]))
					else: continue
				else:
					if (b_aggregate_same_key): dict_data[lst_data[0]] = [0 if len(lst_data) == 1 else (int(lst_data[1]) if b_convert_value_to_int else lst_data[1])]
					else: dict_data[lst_data[0]] = 0 if len(lst_data) == 1 else (int(lst_data[1]) if b_convert_value_to_int else lst_data[1])
		return dict_data
	
	def copy_file(self, sz_file_from, sz_file_to):
		""" copy a file, make a directory if does not exist"""
		if os.path.exists(sz_file_from):
			self.make_path(os.path.dirname(sz_file_to))
			cmd = "cp " + sz_file_from + " " + sz_file_to
			exist_status = os.system(cmd)
			if (exist_status != 0):
				raise Exception("Fail to copy file") 
			
			### set attributes to file 664
			os.chmod(sz_file_to, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IWGRP | stat.S_IROTH)
	
	def move_file(self, sz_file_from, sz_file_to):
		""" copy a file, make a directory if does not exist"""
		if os.path.exists(sz_file_from):
			self.make_path(os.path.dirname(sz_file_to))
			cmd = "mv " + sz_file_from + " " + sz_file_to
			exist_status = os.system(cmd)
			if (exist_status != 0):
				raise Exception("Fail to copy file") 
			
			### set attributes to file 664
			os.chmod(sz_file_to, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IWGRP | stat.S_IROTH)

	def get_temp_file(self, file_name, sz_type):
		"""
		return a temp file name
		"""
		main_path = os.path.join(self.temp_dir, getpass.getuser(), self.project_name)
		if (not os.path.exists(main_path)): os.makedirs(main_path)
		else:
			cmd = "touch {}".format(main_path)
			os.system(cmd)
			
		while 1:
			return_file = os.path.join(main_path, file_name + "_" + str(random.randrange(10000000, 99999999, 10)) + sz_type)
			if (os.path.exists(return_file)): continue
			try:
				os.close(os.open(return_file, os.O_CREAT | os.O_EXCL))
				return return_file
			except FileExistsError:
				pass
	
	def get_temp_file_with_path(self, main_path, file_name, sz_type):
		"""
		return a temp file name
		"""
		if (not os.path.exists(main_path)): os.makedirs(main_path)
		while 1:
			return_file = os.path.join(main_path, file_name + "_" + str(random.randrange(10000000, 99999999, 10)) + sz_type)
			if (os.path.exists(return_file)): continue
			try:
				os.close(os.open(return_file, os.O_CREAT | os.O_EXCL))
				return return_file
			except FileExistsError:
				pass
			
	def get_temp_dir_passing_root_path(self, root_path):
		"""
		return a temp directory
		"""
		if (root_path != self.get_main_path()): main_path = root_path
		else: main_path = self.get_main_path()

		if (not os.path.exists(main_path)): os.makedirs(main_path)
		while 1:
			return_path = os.path.join(main_path, "dir_" + str(random.randrange(100000000, 999999999, 10)))
			if (not os.path.exists(return_path)):
				os.makedirs(return_path)
				return return_path

	def get_temp_dir(self):
		"""
		return a temp directory
		"""
		return self.get_temp_dir_passing_root_path(self.get_main_path())

	def get_main_path(self):
		return os.path.join(self.temp_dir, getpass.getuser(), self.project_name)

	def make_path(self, path_name):
		if (len(path_name) > 0 and not os.path.isdir(path_name) and not os.path.isfile(path_name)):
			cmd = "mkdir -p " + path_name
			os.system(cmd)
			exist_status = os.system(cmd)
			if (exist_status != 0):
				raise Exception("Fail to make a path") 


	def test_file_exists(self, file_name):
		if (os.path.exists(file_name)): return file_name
		sys.exit("Error: file does not exist - " + file_name)

	def remove_file(self, file_name):
		if (not file_name is None and os.path.exists(file_name)): os.unlink(file_name)
	
	def remove_dir(self, path_name):
		if (not path_name is None and os.path.isdir(path_name)):
			main_path = self.get_main_path()
			if path_name == main_path or path_name == (main_path + "/"): cmd = "rm -r {}/*".format(path_name)
			else: cmd = "rm -r {}*".format(path_name)
			os.system(cmd)

	def unzip(self, file_from, file_to):
		"""
		unzip files
		"""
		cmd = "gzip -cd {} > {}".format(file_from, file_to)
		exist_status = os.system(cmd)
		if (exist_status != 0):
			raise Exception("Fail to unzip file: {}".format(cmd)) 

	def compress_file(self, file_from, file_to):
		"""
		compress file
		"""
		cmd = "gzip -c {} > {}".format(file_from, file_to)
		exist_status = os.system(cmd)
		if (exist_status != 0):
			raise Exception("Fail to unzip file: {}".format(cmd)) 

	
	def is_fasta(self, sz_file_name):
		"""
		Test Fata file
		"""
		if (not os.path.exists(sz_file_name)): raise IOError(_("Error: File doens't exist: "  + sz_file_name))
		handle = open(sz_file_name)
		b_pass = False
		for line in handle:
			sz_temp = line.strip()
			if (len(sz_temp) == 0): continue
			if (sz_temp[0] == ">"): 
				b_pass = True
				break
			else: 
				handle.close()
				raise IOError(_("Error: the file is not in FASTA format."))
		handle.close()
		if (not b_pass): raise IOError(_("Error: file is not in FASTA format."))

		record_dict = SeqIO.index(sz_file_name, "fasta")
		if (len(record_dict) > 0): return len(record_dict)
		raise IOError("Error: file is not in FASTA format.")


	def read_text_file(self, file_name):
		"""
		read text file and put the result in an vector
		"""
		if (not os.path.exists(file_name)):
			raise IOError(_("Error: file '" + file_name + "' doens't exist."))
		
		vect_out = []
		with open(file_name) as handle: 
			for line in handle:
				sz_temp = line.strip()
				if (len(sz_temp) == 0): continue
				vect_out.append(sz_temp)
		return vect_out


	def is_gzip(self, file_name): 
		"""
		test if the file name ends in gzip
		"""
		return True if (file_name.rfind(".gz") == len(file_name) - 3) else False
	
	def get_file_name_without_extension(self, file_name):
		"""
		return file name without extension
		"""
		return os.path.splitext(os.path.basename(file_name))[0]

	
	### return (b_value, b_is_correct, sz_error_message)
	def get_bool_from_string(self, sz_value):
		vect_values_true = ["true", "True", "TRUE", "1", "t"]
		vect_values_false = ["false", "False", "FALSE", "0", "f"]
		for true_temp_ in vect_values_true: 
			if (sz_value == true_temp_): return (True, True, "")
		for false_temp_ in vect_values_false: 
			if (sz_value == false_temp_): return (False, True, "")
		return (False, False, "Error: only this values available for bool type (%s;%s), this is not valid %s" % (",".join(vect_values_true), ",".join(vect_values_false), sz_value))

	
	def str2bool(self, v):
		"""
		str to bool
		"""
		return v.lower() in ("yes", "true", "t", "1", "y")



class NucleotideCodes(object):
	
	def __init__(self):
		self.dt_codes = {'A': ['A'], 
						'C' : ['C'],
						'G' : ['G'],
						'T' : ['T', 'U'],
						'U' : ['T', 'U'],
						'R' : ['A', 'G'],
						'Y' : ['C', 'T'],
						'S' : ['G', 'C'],
						'W' : ['A', 'T'],
						'K' : ['G', 'T'],
						'M' : ['A', 'C'],
						'B' : ['C', 'G', 'T'],
						'D' : ['A', 'G', 'T'],
						'H' : ['A', 'C', 'T'],
						'V' : ['A', 'C', 'G'],
						'N' : ['A', 'C', 'G', 'T', 'U'],
					}

	def has_this_base(self, base_ref, base_test):
		return base_ref.upper() in self.dt_codes and base_test.upper() in self.dt_codes[base_ref.upper()]


class CigarElement(object):
	"""
	1) Op
	2) BAM
	3) Description 
	4) Consumes query
	5) Consumes reference
	
	1 2 3                                                     4   5
	M 0 alignment match (can be a sequence match or mismatch) yes yes
	I 1 insertion to the reference yes no
	D 2 deletion from the reference no yes
	N 3 skipped region from the reference no yes
	S 4 soft clipping (clipped sequences present in SEQ) yes no
	H 5 hard clipping (clipped sequences NOT present in SEQ) no no
	P 6 padding (silent deletion from padded reference) no no
	= 7 sequence match yes yes
	X 8 sequence mismatch yes yes
	"""
	
	CIGAR_TAG_M = 'M'
	CIGAR_TAG_S = 'S'
	CIGAR_TAG_I = 'I'
	CIGAR_TAG_D = 'D'
	CIGAR_TAG_H = 'H'

	### add all tags that can be parsed
	DICT_CIGAR_TAGS = { CIGAR_TAG_M : 1, CIGAR_TAG_S : 1, CIGAR_TAG_I : 1, CIGAR_TAG_D : 1,\
				CIGAR_TAG_H : 1 }

	def __init__(self, length, tag):
		self.length = length
		self.tag = tag

	def is_M(self): return self.tag == CigarElement.CIGAR_TAG_M
	def is_S(self): return self.tag == CigarElement.CIGAR_TAG_S
	def is_I(self): return self.tag == CigarElement.CIGAR_TAG_I
	def is_D(self): return self.tag == CigarElement.CIGAR_TAG_D
	def is_H(self): return self.tag == CigarElement.CIGAR_TAG_H

	def __str__(self):
		return "{} -> {}".format(self.tag, self.length)

class CountLength(object):
	
	def __init__(self):
		self.length_query = 0
		self.length_subject = 0
		self.miss_match = 0

	
	def __add__(self, other):
		""" add values """
		self.length_query += other.length_query
		self.length_subject += other.length_subject
		self.miss_match += other.miss_match
		return self


	def __gt__(self, other):
		return (self.length_query + self.length_subject) > (other.length_query + other.length_subject)


	def add(self, other, possible_overlap, possible_previous_overlap):
		"""
		add 
		"""
		self.length_query += other.length_query
		self.length_subject += other.length_subject
		self.miss_match += other.miss_match
		if (not possible_previous_overlap is None):
			possible_remove_query = possible_previous_overlap.end_query - possible_overlap.start_query + 1
			possible_remove_subject = possible_previous_overlap.end_subject - possible_overlap.start_subject + 1
			if (possible_remove_query > 0): self.length_query -= possible_remove_query
			if (possible_remove_subject > 0): self.length_subject -= possible_remove_subject

	def __str__(self):
		return "{}\t{}\t{}".format(self.length_query, self.length_subject, self.miss_match)

	def get_lenth_query(self):
		return self.length_query
	
	def get_lenth_subject(self):
		return self.length_subject

	def get_header(self):
		""" return header for __str__ return """
		return "length query\tlength subject\tmissmatch"
			
	def clean_count(self):
		""" clean all counts """
		self.length_query = 0
		self.length_subject = 0
		self.miss_match = 0
		
	def count_cigar(self, vect_cigar_element):
		"""
		:param vect_cigar_element[ vect [<CigarElement>] ]
		"""
		for vect_cigar in vect_cigar_element:
			for cigar_element in vect_cigar:
				if cigar_element.is_M():
					self.length_query += cigar_element.length
					self.length_subject += cigar_element.length
				elif cigar_element.is_I():
					self.length_subject += cigar_element.length
				elif cigar_element.is_D():
					self.length_query += cigar_element.length
				else:		### S or ### H
					self.miss_match += cigar_element.length

	
	def get_percentage_coverage(self, length_chr1, length_chr2):
		"""
		:out percetnage coverage
		"""
		return ((self.length_query + self.length_subject) / float(length_chr1 + length_chr2)) * 100.0

	def is_100_percent(self, length_chr1, length_chr2):
		"""
		:out True if 100%
		"""
		return int(self.get_percentage_coverage(length_chr1, length_chr2)) == 100
		
		
class Cigar(object):

	#### utils
	utils = Utils()
	
	def __init__(self, vect_cigar_string, keep_best = False):
		"""
		:param only keep the best alignment
		"""
		self.vect_cigar_string = vect_cigar_string
		self.vect_positions = []
		self.keep_best = keep_best
		self.index_best_alignment = -1		### if keep_best this variable has the index of best alignment
		self.count_length = CountLength()
		self._parse_cigar()
	
	def __str__(self):
		return "\n".join(self.vect_cigar_string)
	
	def _parse_cigar(self):
		"""
		parse cigar string "53S487M60I26M1D69M3I90M1D130M3I318M"
		"""
		position = ""
#		print(self.vect_cigar_string)

		for cigar_string in self.vect_cigar_string:
			vect_positions = []
			for _ in range(len(cigar_string)):
				if (self.utils.is_integer(cigar_string[_])):
					position += cigar_string[_]
				else:
					if not cigar_string[_] in CigarElement.DICT_CIGAR_TAGS:
						raise Exception("Error: this tag'{}' i not recognized in the parse filter.".format(cigar_string[_]))
					vect_positions.append(CigarElement(int(position), cigar_string[_]))
					position = ""
			self.vect_positions.append(vect_positions)
		
		### count match positions in query and subject
		self.count_length.clean_count()
		if (self.keep_best):
			self.index_best_alignment = -1
			count_element_best = CountLength()
			for _ in range(len(self.vect_positions)):
				count_length_to_test = CountLength()
				count_length_to_test.count_cigar([self.vect_positions[_]])
				
				if (count_length_to_test > count_element_best):
					count_element_best = count_length_to_test
					self.index_best_alignment = _
				
			self.count_length = count_element_best
		else:
			self.count_length.count_cigar(self.vect_positions)

	def get_count_element(self):
		return self.count_length
	
	def get_number_cigar_string(self):
		return len(self.vect_cigar_string)

	def get_vect_cigar_string(self):
		"""
		:out all cigar strings
		"""
		return self.vect_cigar_string

	def get_best_vect_cigar_elements(self):
		"""
		"""
		### only do the last
		if (self.index_best_alignment != -1): return self.vect_positions[self.index_best_alignment]
		else: return self.vect_positions[-1]
		
	def get_position_from_2_to(self, position):
		"""
		:param position, position "from" at one base in first sequence (source A)
		:returns (position in second sequence (hit B), if does not have position return left most position)
			-1 to no position
		"""
		
		if (position < 1): return (-1, -1)
		##for vect_positions in self.vect_positions:
		
		### only do the best
		vect_positions = self.get_best_vect_cigar_elements()
		
		b_insert_position = False
		real_position_to = 0			### sequence a
		real_position_from = -1			### sequence b
		left_most_position = -1
		
		(position_on_hit, left_position_on_hit) = (-1, -1)		### default return
		for cigar_element in vect_positions:
#			print(cigar_element)
			if cigar_element.is_M():
				if (real_position_from == -1): real_position_from = 0 
				real_position_to += cigar_element.length
				real_position_from += cigar_element.length
				b_insert_position = False
			elif cigar_element.is_D():
				if (real_position_to > 0): left_most_position = real_position_to
				if (real_position_from == -1): real_position_from = 0
				#real_position_to += cigar_element.length
				real_position_from += cigar_element.length
				b_insert_position = True
			elif cigar_element.is_I():
				real_position_to += cigar_element.length
				#real_position_from += cigar_element.length
				b_insert_position = False
			else:		### S or ### H
				if (real_position_to > 0): left_most_position = real_position_to
				real_position_to += cigar_element.length
				#real_position_from += cigar_element.length
				b_insert_position = True

			if (position <= real_position_from):
				if (b_insert_position): (position_on_hit, left_position_on_hit) = (-1, left_most_position)
#				print("position:{}  real_position_to:{}  real_position_from:{}".format(position, real_position_to, real_position_from))
				elif (real_position_from > 0): (position_on_hit, left_position_on_hit) =  (position + (real_position_to - real_position_from), -1)
				else: (position_on_hit, left_position_on_hit) = (-1, -1)
				break
		
		### try if there's any result yet
		if (position_on_hit != -1): return (position_on_hit, left_position_on_hit)
			
		return (position_on_hit, left_position_on_hit)


