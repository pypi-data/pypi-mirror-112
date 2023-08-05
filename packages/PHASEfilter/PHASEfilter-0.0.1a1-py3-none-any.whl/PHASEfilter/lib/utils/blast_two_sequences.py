'''
Created on 20/05/2020

@author: mmp
'''
import os
from PHASEfilter.lib.utils.util import Utils, Cigar, CountLength
from PHASEfilter.lib.utils.software import Software

class BlastDescritpion(object):
	
	def __init__(self):
		self.sequence = []	### need to be array because of replace bases
		self.vect_holes = None

	def add_sequence(self, sequence):
		self.sequence.extend(list(sequence))
	
	def has_dash(self):
		"""
		:out True if it has dash
		"""
		if (self.vect_holes is None): self.get_holes()
		return len(self.vect_holes) > 0

	def get_length(self):
		"""
		:out len of the sequence
		"""
		return len(self.sequence)

	def get_holes(self):
		"""
		get a vector with holes positions
		"""
		if (self.vect_holes is None):
			self.vect_holes = []
			try:
				index = self.sequence.index('-')
			except ValueError:
				index = -1

			while index != -1:
				self.vect_holes.append(index)
				try:
					index = self.sequence.index('-', index + 1)
				except ValueError:
					index = -1
		return self.vect_holes

	def get_next_base(self, position):
		"""
		:out base after the position in parameter, empty if doesn't have, and position
		"""
		for _ in range(position + 1, len(self.sequence)):
			if (self.sequence[_] != '-'): return (self.sequence[_], _)
		return ("", -1)

	def get_base(self, position):
		return self.sequence[position] if position < len(self.sequence) else -1

	def set_base(self, next_based, position):
		self.sequence[position] = next_based

	def get_sequence(self):
		return "".join(self.sequence)



class SyncHoles(object):
	
	QUERY = 0
	SUBJECT = 1
	def __init__(self, position, type_):
		self.position = position
		self.type_ = type_
		
	def is_query(self):
		return self.type_ == SyncHoles.QUERY

	def __eq__(self, other):
		return self.position == other.position and self.type_ == other.type_

	def __str__(self):
		return "Position: {}   type: {}".format(self.position,
			"Query" if self.type_ == SyncHoles.QUERY else "Hole")

class SynchronizeSequence(object):

	def __init__(self):
		self.vect_data = []
	
	def add_vector_query(self, vect_query):
		self.vect_data.extend([SyncHoles(_, SyncHoles.QUERY) for _ in vect_query])
	
	def add_vector_subject(self, vect_query):
		self.vect_data.extend([SyncHoles(_, SyncHoles.SUBJECT) for _ in vect_query])

	def sort_data(self):
		self.vect_data = sorted(self.vect_data, key=lambda x : x.position)

	def clean_all(self):
		self.vect_data = []
		
class BlastAlignment(object):
	
	def __init__(self, debug = False, use_multithreading = True):
		self.use_multithreading = use_multithreading
		
		self.query = BlastDescritpion()
		self.subject = BlastDescritpion()
		self.match = BlastDescritpion()
		
		self.synchronize = SynchronizeSequence()
		self.start_query = -1
		self.end_query = -1
		self.start_subject = -1
		self.end_subject = -1
		self.cigar = None
		self.debug = debug


	def add_query(self, pos_from, sequence, pos_to):
		if (self.start_query == -1): self.start_query = pos_from
		self.end_query = pos_to
		self.query.add_sequence(sequence)
	def add_subject(self, pos_from, sequence, pos_to):
		if (self.start_subject == -1): self.start_subject = pos_from
		self.end_subject = pos_to
		self.subject.add_sequence(sequence)
	def add_match(self, match):
		self.match.add_sequence(match)

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
	
	def _get_fixed_base(self, index_synchronize):
		if (self.synchronize.vect_data[index_synchronize].is_query()):
			return self.subject.get_base(self.synchronize.vect_data[index_synchronize].position)
		else:
			return self.query.get_base(self.synchronize.vect_data[index_synchronize].position)
	
	def _get_next_base(self, index_synchronize):
		"""
		:out ((next_based, next_based_oposed, position))
		"""
		if (self.synchronize.vect_data[index_synchronize].is_query()):
			(next_based, position) = self.query.get_next_base(self.synchronize.vect_data[index_synchronize].position)
			return (next_based, self.subject.get_base(position), position)
		else:
			(next_based, position) = self.subject.get_next_base(self.synchronize.vect_data[index_synchronize].position)
			return (next_based, self.query.get_base(position), position)

	def _swap_base(self, index_synchronize, next_based, position):
		if (self.synchronize.vect_data[index_synchronize].is_query()):
			self.query.set_base("-", position)
			self.query.set_base(next_based, self.synchronize.vect_data[index_synchronize].position)
			self._add_position_in_index(index_synchronize, \
				self.synchronize.vect_data[index_synchronize].position)
		else:
			self.subject.set_base("-", position)
			self.subject.set_base(next_based, self.synchronize.vect_data[index_synchronize].position)
			self._add_position_in_index(index_synchronize, \
				self.synchronize.vect_data[index_synchronize].position)
	##		self.synchronize.vect_data[index_synchronize].position += 1
			
	def _add_position_in_index(self, index_synchronize, position):
		"""
		Add position in tandem
		"""
# 		print("length: ", len(self.synchronize.vect_data), "index: ", index_synchronize,
# 			"position: ", self.synchronize.vect_data[index_synchronize].position)
# 		if (len(self.synchronize.vect_data) > (index_synchronize + 1)):
# 			print("position +1 index: ", self.synchronize.vect_data[index_synchronize + 1].position)
			
		if (len(self.synchronize.vect_data) > (index_synchronize + 1) and 
			self.synchronize.vect_data[index_synchronize + 1].position == (position + 1)):
			self._add_position_in_index(index_synchronize + 1, position + 1)
		self.synchronize.vect_data[index_synchronize].position += 1
		
	def _shift_left_base(self, index_synchronize):
		
		fixed_based = self._get_fixed_base(index_synchronize)
		(next_based, next_based_oposed, position) = self._get_next_base(index_synchronize)
		shift_bases = 0
		while (fixed_based == next_based) or (fixed_based == next_based_oposed):
			self._swap_base(index_synchronize, next_based, position)
			fixed_based = self._get_fixed_base(index_synchronize)
			(next_based, next_based_oposed, position) = self._get_next_base(index_synchronize)
			shift_bases += 1
		return shift_bases

	def get_query_sequence(self):
		return self.query.get_sequence()
	
	def get_subject_sequence(self):
		return self.subject.get_sequence()
		
	def syncronize_data(self):
		"""
		"""
		self.synchronize.clean_all()
		self.synchronize.add_vector_query(self.query.get_holes())
		self.synchronize.add_vector_subject(self.subject.get_holes())
		self.synchronize.sort_data()

	def make_cigar_string(self):
		"""
		create cigar string
		"""
		
		### TODO create threading 
		self.syncronize_data()
		
		cigar = ""
		deletion = 0
		insertion = 0
		last_postion = 0
		
		for _ in range(len(self.synchronize.vect_data)):
			shift_bases = self._shift_left_base(_)	## to shift left
			if (self.synchronize.vect_data[_].is_query()):
				if (deletion > 0): cigar += "{}D".format(deletion)
				if (insertion > 0 and self.synchronize.vect_data[_].position > last_postion):
					cigar += "{}I".format(insertion)
					cigar += "{}M".format(self.synchronize.vect_data[_].position - last_postion)
					insertion = 0
				elif (self.synchronize.vect_data[_].position - last_postion > 0):
					cigar += "{}M".format(self.synchronize.vect_data[_].position - last_postion)
				
				deletion = 0
				insertion += 1
				last_postion = self.synchronize.vect_data[_].position + 1
			else:
				if (insertion > 0): cigar += "{}I".format(insertion)
				if (deletion > 0 and self.synchronize.vect_data[_].position > last_postion):
					cigar += "{}D".format(deletion)
					cigar += "{}M".format(self.synchronize.vect_data[_].position - last_postion)
					deletion = 0
				elif (self.synchronize.vect_data[_].position - last_postion > 0):
					cigar += "{}M".format(self.synchronize.vect_data[_].position - last_postion)
				
				insertion = 0
				deletion += 1
				last_postion = self.synchronize.vect_data[_].position + 1
		
		### get last match
		if (deletion > 0): cigar += "{}D".format(deletion)
		if (insertion > 0): cigar += "{}I".format(insertion)
		if (self.query.get_length() - last_postion > 0):
			cigar += "{}M".format(self.query.get_length() - last_postion)
		
		### position
		self.cigar = Cigar([cigar])
		
		### release memory
		if (not self.debug): self.synchronize.clean_all()
		
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

class Reversor:
	def __init__(self, obj):
		self.obj = obj
	
	def __eq__(self, other):
		return other.obj.end_query == self.obj.end_query
	
	def __lt__(self, other):
		return other.obj.end_query < self.obj.end_query

class ReversorSubject:
	def __init__(self, obj):
		self.obj = obj
	
	def __eq__(self, other):
		return other.obj.end_subject == self.obj.end_subject
	
	def __lt__(self, other):
		return other.obj.end_subject < self.obj.end_subject
	
class VectAlignments(object):

	def __init__(self):
		self.vect_alignments = []
	
	def print_all_alignments(self, b_print_cigar = False):
		"""
		Show all alignments
		"""
		print("\n" + "*" * 50)
		for _ in range(len(self.vect_alignments)):
			if (b_print_cigar):
				print("Make cigar, Query: {}-{}  len({})    Subject: {}-{}  len({})    Cigar:{}".format(
					self.vect_alignments[_].start_query,\
					self.vect_alignments[_].end_query, \
					self.vect_alignments[_].end_query - self.vect_alignments[_].start_query,\
					self.vect_alignments[_].start_subject, self.vect_alignments[_].end_subject,\
					self.vect_alignments[_].end_subject - self.vect_alignments[_].start_subject,\
					",".join(self.vect_alignments[_].get_vect_cigar()) ))
			else:
				print("Make cigar, Query: {}-{}  len({})    Subject: {}-{}  len({})".format(
					self.vect_alignments[_].start_query,\
					self.vect_alignments[_].end_query, \
					self.vect_alignments[_].end_query - self.vect_alignments[_].start_query,\
					self.vect_alignments[_].start_subject, self.vect_alignments[_].end_subject,\
					self.vect_alignments[_].end_subject - self.vect_alignments[_].start_subject))
		print("Total: " + str(len(self.vect_alignments)))


	def remove_overlap_alignments(self):
		"""
		remove overlap alignments
		"""
		
		### remove by query
		self.sort_all_alignments()
		vect_to_remove = []
		for i_1 in range(0, len(self.vect_alignments) -1):
			for i_2 in range(i_1 + 1, len(self.vect_alignments)):
				if (i_2 in vect_to_remove): continue
				if (self.vect_alignments[i_1].start_query <= self.vect_alignments[i_2].start_query and
					self.vect_alignments[i_1].end_query >= self.vect_alignments[i_2].end_query):
					vect_to_remove.append(i_2)
		vect_to_remove = sorted(vect_to_remove, reverse=True)
		for _ in vect_to_remove: del self.vect_alignments[_]

		### remove by subject
		self.sort_all_alignments_subject()
		vect_to_remove = []
		for i_1 in range(0, len(self.vect_alignments) -1):
			for i_2 in range(i_1 + 1, len(self.vect_alignments)):
				if (i_2 in vect_to_remove): continue
				if (self.vect_alignments[i_1].start_subject <= self.vect_alignments[i_2].start_subject and
					self.vect_alignments[i_1].end_subject >= self.vect_alignments[i_2].end_subject):
					vect_to_remove.append(i_2)
		vect_to_remove = sorted(vect_to_remove, reverse=True)
		for _ in vect_to_remove: del self.vect_alignments[_]

		### order by query
		self.sort_all_alignments()

	def sort_all_alignments(self):
		"""
		sort all alignments
		"""
		self.vect_alignments = sorted(self.vect_alignments, key=lambda x : (x.start_query, Reversor(x)) )

	def sort_all_alignments_subject(self):
		"""
		sort all alignments
		"""
		self.vect_alignments = sorted(self.vect_alignments, key=lambda x : (x.start_subject, ReversorSubject(x)) )

	def get_cigar(self, index):
		"""
		:out return cigar string
		"""
		return self.vect_alignments[index].get_cigar() if index < len(self.vect_alignments) else ""

	def get_cigar_strings(self):
		"""
		:out return all cigar strings
		"""
		vect_return = []
		for cigar_element in self.vect_alignments:
			vect_return.extend(cigar_element.get_vect_cigar())
		return vect_return
	
	def get_cigar_count_elements(self):
		"""
		:out return all cigar strings
		"""
		blast_alignment_previous = None
		count_element = CountLength()
		for blast_alignment in self.vect_alignments:
			count_element.add(blast_alignment.get_cigar().get_count_element(),\
				blast_alignment, blast_alignment_previous)
			blast_alignment_previous = blast_alignment
		return count_element
	
	def get_number_cigar_string(self):
		return_value = 0
		for blast_alignment in self.vect_alignments:
			return_value += blast_alignment.get_cigar().get_number_cigar_string()
		return return_value

	def get_position_from_2_to(self, position_query):
		"""
		search for all alignments and try to find
		:out (position in to ref, if does not have position return left most position)
			-1 to no position
		"""
		for _ in range(len(self.vect_alignments)):
			#print("position_query: {}  start:{}   end:{}".format(position_query, self.vect_alignments[_].start_query, self.vect_alignments[_].end_query))
			if (position_query >= self.vect_alignments[_].start_query and \
				position_query <= self.vect_alignments[_].end_query):
				return self.vect_alignments[_].get_position_from_2_to(position_query)
		return (-1, -1)

	def get_number_alignments(self):
		"""
		:out number of the alignments
		"""
		return len(self.vect_alignments)


class BlastAlignments(VectAlignments):
	
	def __init__(self, debug = False, use_multithreading = False):
		VectAlignments.__init__(self)
		
		self.debug = debug
		self.use_multithreading = use_multithreading
		self.dont_add_alignments = True


	def add_new_alignment(self):
		"""
		add new alignment
		"""
		## get star and end position of 
		if (len(self.vect_alignments) > 0): 
			### get cigar string for the last alignment
			self.create_cigar_string()
				
		### add new alignment
		self.vect_alignments.append(BlastAlignment(self.debug, self.use_multithreading))
		self.dont_add_alignments = False


	def set_dont_add_alignments(self):
		self.dont_add_alignments = True


	def add_query(self, query):
		"""
		Query  534929   GAATTGAACTTGTGGTTGTTGATAGCATCATCTTCGTGTTCTCCGTGCTCAGATTCAGCT  534988
		"""
		if (len(self.vect_alignments) == 0 or self.dont_add_alignments): return
		(pos_from, sequence, poss_to) = self._get_info_file(query)
		self.vect_alignments[-1].add_query(pos_from, sequence, poss_to)


	def add_subject(self, subject):
		"""
		Sbjct  534929   GAATTGAACTTGTGGTTGTTGATAGCATCATCTTCGTGTTCTCCGTGCTCAGATTCAGCT  534988
		"""
		if (len(self.vect_alignments) == 0 or self.dont_add_alignments): return
		
		### process last line
		(pos_from, sequence, poss_to) = self._get_info_file(subject)
		self.vect_alignments[-1].add_subject(pos_from, sequence, poss_to)


	def add_match(self, match):
		"""
		Add match "||||||||||||| |||||  ||||||||"
		"""
		if (len(self.vect_alignments) == 0 or self.dont_add_alignments): return
		self.vect_alignments[-1].add_match(match)


	def _get_info_file(self, sz_line):
		"""
		Query  534929   GAATTGAACTTGTGGTTGTTGATAGCATCATCTTCGTGTTCTCCGTGCTCAGATTCAGCT  534988
		OR
		Sbjct  534929   GAATTGAACTTGTGGTTGTTGATAGCATCATCTTCGTGTTCTCCGTGCTCAGATTCAGCT  534988
		:out (from<int>, sequence, to<int>)
		"""
		lst_data = sz_line.split()
		if (len(lst_data) != 4):
			raise Exception("Error: some problem with this blast line\n" + sz_line)
		return (int(lst_data[1]), lst_data[2], int(lst_data[3]))

	def create_cigar_string(self):
		"""
		create CIGAR string from last alignment
		"""

		### get start and end position
		if self.debug:
			print("Make cigar, Query: {}-{} len({})     Subject: {}-{}".format(self.vect_alignments[-1].start_query,\
				self.vect_alignments[-1].end_query,\
				self.vect_alignments[-1].end_query - self.vect_alignments[-1].start_query,\
				self.vect_alignments[-1].start_subject, self.vect_alignments[-1].end_subject))
		self.vect_alignments[-1].make_cigar_string()

		
class BlastTwoSequences(object):
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
		
		temp_file_out = self.utils.get_temp_file("lastz_result", ".txt")
		
		### blastn -query Ca22chr2B_C_albicans_SC5314.fasta -subject ../genomeA/Ca22chr2A_C_albicans_SC5314.fasta -dust no -evalue 1e-5 > result.blastn
		cmd = "{} -query {} -subject {} -dust no -evalue 1e-5 > {}".format(\
			self.software.get_blast(), self.file_a, self.file_b, temp_file_out)
		exist_status = os.system(cmd)
		if (exist_status != 0):
			self.utils.remove_file(temp_file_out)
			raise Exception("Fail to run blastn.\n" + cmd)
		return temp_file_out

	def align_data(self):
		"""
		"""
		
		### hold all blast alignments
		blast_alignments = BlastAlignments(self.debug, self.use_multithreading)
		
		### get blast result
		temp_file_out = self._process_files()
		
		query_processed = False
		### parse file
		with open(temp_file_out) as handle:
			for line in handle:
				sz_temp = line.strip()
				if (len(sz_temp) == 0): continue
				if (sz_temp.startswith("Strand=")):
					
					### add new alignment
					if (sz_temp.replace("Strand=", "").split("/")[0] == "Plus" and
						sz_temp.replace("Strand=", "").split("/")[1] == "Plus"):
						### add new alignment
						blast_alignments.add_new_alignment()
					else:
						### to don't allow set new queries and subjects
						blast_alignments.set_dont_add_alignments()
						
				elif (sz_temp.startswith("Query=")): continue
				elif (sz_temp.startswith("Query")):
					blast_alignments.add_query(sz_temp)
					query_processed = True
				elif (query_processed):
					# don't need this information
					# blast_alignments.add_match(sz_temp)
					query_processed = False
				elif (sz_temp.startswith("Sbjct")):
					blast_alignments.add_subject(sz_temp)
		
		### create cigar string for last alignment
		blast_alignments.create_cigar_string()
		
		### sort alignments
		blast_alignments.remove_overlap_alignments()
		blast_alignments.print_all_alignments()

		### remove tmp file 
		self.utils.remove_file(temp_file_out)
		return blast_alignments



