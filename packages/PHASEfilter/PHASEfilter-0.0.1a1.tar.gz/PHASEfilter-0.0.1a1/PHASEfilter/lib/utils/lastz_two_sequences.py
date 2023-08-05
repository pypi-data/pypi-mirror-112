'''
Created on 29/05/2020

@author: mmp
'''
import os
from PHASEfilter.lib.utils.util import Utils, Cigar
from PHASEfilter.lib.utils.software import Software
from PHASEfilter.lib.utils.blast_two_sequences import VectAlignments

class LastzAlignment(object):
	
	def __init__(self, debug = False, use_multithreading = True):
		self.use_multithreading = use_multithreading
		
		self.start_query = -1
		self.end_query = -1
		self.start_subject = -1
		self.end_subject = -1
		self.cigar = None
		self.debug = debug


	def add_line(self, line_from_file_out):
		"""
		format name1,start1,end1,name2,start2,end2,strand2,cigar
		"""
		lst_data = line_from_file_out.strip().split()
		if (len(lst_data) == 8):
			self.start_query = int(lst_data[1])
			self.end_query = int(lst_data[2])
			self.start_subject = int(lst_data[4])
			self.end_subject = int(lst_data[5])
			self.cigar = Cigar([lst_data[7]])
		
	def get_start_end_positions(self):
		"""
		:out start and end position for query and subject
		"""
		return (self.start_query, self.end_query, self.start_subject, self.end_subject)

	def get_cigar(self):
		"""
		:out get cigar
		"""
		return self.cigar

	def get_vect_cigar(self):
		"""
		:out 
		"""
		return self.cigar.vect_cigar_string
	
	def get_position_from_2_to(self, position):
		"""
		:out (position in to ref, if does not have position return left most position)
			-1 to no position
		"""
		##
		if (self.start_query > position or self.end_query < position): return (-1, -1)
		(position_on_hit, left_position_on_hit) = self.cigar.get_position_from_2_to(position - self.start_query + 1)
		return (position_on_hit + self.start_query - 1 + (self.start_subject - self.start_query) if position_on_hit != -1 else -1,\
			left_position_on_hit + self.start_query - 1 + (self.start_subject - self.start_query) if left_position_on_hit != -1 else -1)


class LastzAlignments(VectAlignments):
	
	def __init__(self, debug = False, use_multithreading = False):
		VectAlignments.__init__(self)
		self.debug = debug
		self.use_multithreading = use_multithreading
		self.dont_add_alignments = True


	def add_new_alignment(self, line_from_file_out):
		"""
		add new alignment
		"""
				
		### add new alignment
		self.vect_alignments.append(LastzAlignment(self.debug, self.use_multithreading))
		self.vect_alignments[-1].add_line(line_from_file_out)


class LastzTwoSequences(object):
	'''
	Blast two sequences and create a cigar string from the result
	'''

	utils = Utils()
	software = Software()

	def __init__(self, file_a, file_b, debug = False, use_multithreading = False):
		'''
		Constructor
		'''
		self.file_a = file_a
		self.file_b = file_b
		self.debug = debug
		self.use_multithreading = use_multithreading

	def _process_files(self):
		"""
		"""
		
		temp_file_out = self.utils.get_temp_file("blast_result", ".txt")
		
		### /home/software/lastz/src/lastz /tmp/mmp/synchronize/chr_file_chrIII_16424400.fasta /tmp/mmp/synchronize/chr_file_chrIII_36592820.fasta --format=general:name1,start1,end1,name2,start2,end2,strand2,cigar --strand=plus --output=/tmp/mmp/generic/blast_result_61739140.txt --ambiguous=iupac
		### /home/software/lastz/src/lastz ../genomeA/Ca22chr1A_C_albicans_SC5314.fasta Ca22chr1B_C_albicans_SC5314.fasta --format=general:name1,start1,end1,name2,start2,end2,strand2,cigar --strand=plus --output=temp1.txt --ambiguous=iupac
		cmd = "{} {} {} --format=general:name1,start1,end1,name2,start2,end2,strand2,cigar --strand=plus --output={} --ambiguous=iupac".format(\
			self.software.get_lastz(), self.file_a, self.file_b, temp_file_out)
		exist_status = os.system(cmd)
		if (exist_status != 0):
			self.utils.remove_file(temp_file_out)
			raise Exception("Fail to run lastz.\n" + cmd)
		return temp_file_out

	def align_data(self):
		"""
		align two fasta files
		"""
		
		### hold all blast alignments
		lastz_alignments = LastzAlignments(self.debug, self.use_multithreading)
		
		### get blast result
		temp_file_out = self._process_files()
		
		### parse file
		## <name1> <start1> <end1> <name2> <start2> <end2> <strand2> [<score>] [#<comment>]
		## where <name1>, etc. correspond to the target sequence and <name2>, etc. correspond to the query. Fields are delimited by whitespace. 
		with open(temp_file_out) as handle:
			for line in handle:
				sz_temp = line.strip()
				if (len(sz_temp) == 0 or sz_temp.startswith('#')): continue
				### add new alignments
				lastz_alignments.add_new_alignment(sz_temp)
		
		### sort alignments
#		lastz_alignments.print_all_alignments()
		lastz_alignments.remove_overlap_alignments()
		lastz_alignments.print_all_alignments()

		### remove tmp file 
		self.utils.remove_file(temp_file_out)
		return lastz_alignments



