'''
Created on 06/12/2019

@author: mmp
'''
from PHASEfilter.lib.utils.util import Utils
from PHASEfilter.lib.utils.reference import Reference
from PHASEfilter.lib.utils.lift_over_simple import LiftOverLight
from PHASEfilter.lib.utils.run_extra_software import RunExtraSoftware
from PHASEfilter.lib.utils.read_gff import ReadGFF
from PHASEfilter.lib.utils.software import Software
from PHASEfilter.lib.utils.vcf_process import VcfProcess
from PHASEfilter.lib.utils.testing_software import SoftwareTest
from operator import itemgetter
import os

class ProcessTwoReferences(object):
	
	utils = Utils("synchronize")
	run_extra_software = RunExtraSoftware()
	
	def __init__(self, reference_1, reference_2, outfile, out_path_alignments = None):
		"""
		set the data
		"""
		### read references
		self.reference_1 = Reference(reference_1)
		self.reference_2 = Reference(reference_2)
		self.outfile = outfile
		self.out_path_alignments = out_path_alignments

	def process(self, vect_pass_ref = []):
		"""
		:param vect_pass_ref - chromosomes to not process
		compare the alignments available
		"""
		print("\nStart processing....")
				
		### Process one chr at time 
		vect_process_B = []
		vect_not_process_A = []
		temp_work_dir = self.utils.get_temp_dir()
		
		with open(self.outfile, 'w') as handle_write:
			handle_write.write("Source genome\t{}\nHit genome\t{}\n\nSource genome\tHit genome\nChromosomes\tChromosomes\t".format(\
					self.reference_1.get_reference_name(),\
					self.reference_2.get_reference_name())\
					+ "Software\tGragment split\tLength Match Source\tLength Source\tLength Match Hit\tLength Hit\tAlignment %\tBest\n")
			
			for chr_name_A in self.reference_1.vect_reference:
				if (chr_name_A.lower() in vect_pass_ref):
					print("Waning: this chr '{}' is not going to be processed".format(chr_name_A))
					vect_not_process_A.append(chr_name_A)
					continue
				
				chr_name_B = self.reference_2.get_chr_in_genome(chr_name_A)
				if chr_name_B is None: 
					vect_not_process_A.append(chr_name_A)
					continue
				vect_process_B.append(chr_name_B)

				### processing chromosomes
				self._process_chromosome(chr_name_A, chr_name_B, handle_write)
				
		### print chr not process
		vect_not_processed_B = self.reference_2.chr_not_included(vect_process_B)
		vect_not_processed_A = vect_not_process_A
		if (len(vect_not_processed_A) == 0): print("All chromosomes are processed for genome 1")
		else: print("Warning: chromosomes not processed for {}: ['{}']".format(self.reference_1.get_reference_name(), "', '".join(vect_not_processed_A)))
		if (len(vect_not_processed_B) == 0): print("All chromosomes are processed for genome 2")
		else: print("Warning: chromosomes not processed for {}: ['{}']".format(self.reference_2.get_reference_name(), "', '".join(vect_not_processed_B)))
	
		### remove tmp files
		self.utils.remove_dir(temp_work_dir)
			
		### print info
		print("Report result: {}".format(self.outfile))
	
	
	def _process_chromosome(self, chr_name_A, chr_name_B, handle_write):
		"""
		process by chromosome
		"""
		print("Start processing {} chr: {} ->  {} chr: {}".format(self.reference_1.get_reference_name(),\
					chr_name_A, self.reference_2.get_reference_name(), chr_name_B))
		handle_write.write("{}\t{}\t".format(chr_name_A, chr_name_B))
		
		temp_work_dir = self.utils.get_temp_dir()
		
		lift_over_ligth = LiftOverLight(self.reference_1, self.reference_2, temp_work_dir)
		lift_over_ligth.synchronize_sequences_all_methods(chr_name_A, chr_name_B)
		
		vect_out = []
		for software in Software.VECT_SOFTWARE_DO_ALIGNMENT:
			count_elements = lift_over_ligth.get_count_cigar_length(software, chr_name_A, chr_name_B)
			
			if (count_elements == None):
				vect_out.append([software, 0.0])
			else:
				vect_out.append(["{}\t{}\t{}\t{}\t{}\t{}\t{:.2f}".format(software, \
					lift_over_ligth.get_number_cigar_string(software, chr_name_A, chr_name_B),\
					count_elements.get_lenth_query(), self.reference_1.get_chr_length(chr_name_A),\
					count_elements.get_lenth_subject(), self.reference_2.get_chr_length(chr_name_B),\
					count_elements.get_percentage_coverage(self.reference_1.get_chr_length(chr_name_A),\
						self.reference_2.get_chr_length(chr_name_B)) ),
					float(count_elements.get_percentage_coverage(self.reference_1.get_chr_length(chr_name_A),\
						self.reference_2.get_chr_length(chr_name_B))) ])
				
				### save the alignment in file
				if (not self.out_path_alignments is None):
					print("########   ", software)
					## lastz does not have CIGAR strings
					if (software == 'lastz'): continue
					if (software == 'blastn'): continue
					
					path_out = os.path.join(self.out_path_alignments, software)
					if not os.path.exists(path_out): os.makedirs(path_out)
					file_out = os.path.join(path_out, "{}_{}.aln".format(chr_name_A, chr_name_B))
					lift_over_ligth.create_alignment_file(file_out, software, chr_name_A, chr_name_B)
				
		### sort
		vect_out = sorted(vect_out, key=itemgetter(1), reverse=True)
		
		### get index best values
		vect_best = []
		best_value = 0.0
		for _, values in enumerate(vect_out):	### get best
			if values[1] > 0 and best_value <= values[1]:
				best_value = values[1]
				vect_best.append(_)
		
		### save data
		for _, line in enumerate(vect_out):
			if (_ > 0): handle_write.write("\t\t")
			handle_write.write("{}{}\n".format(line[0], "\t*" if _ in vect_best else ""))
		
		### remove temp files
		self.utils.remove_dir(temp_work_dir)
		print("Processed {} chr: {} ->  {} chr: {}".format(self.reference_1.get_reference_name(),\
					chr_name_A, self.reference_2.get_reference_name(), chr_name_B))
		
		
	def parse_gff(self, gff_file_to_parse, vect_pass_ref, vect_type_to_process):
		"""
		:param gff_file_to_parse file gff3 to parse
		:param vect_pass_ref = vector with chromosomes names to not procesee 
		:param vect_type_to_process = [ReadGFF.PROCESS_TYPE_all] or gene,transcript,... other
		Set new tags in GFF3 files with hit position
		Tag add: StartHit and EndHit
		"""
		print("Start processing {} -> {}".format(self.reference_1.get_reference_name(),\
					self.reference_2.get_reference_name()))

		temp_work_dir = self.utils.get_temp_dir()		
		impose_minimap2_only = False
		lift_over_ligth = LiftOverLight(self.reference_1, self.reference_2, temp_work_dir, impose_minimap2_only, False)
		
		read_gff = ReadGFF(gff_file_to_parse)
		(lines_parsed, lines_failed_parse, vect_fail_synch) = read_gff.parse_gff(self.outfile, vect_type_to_process, vect_pass_ref, lift_over_ligth)
		
		print("Lines parsed: {}   Lines Failed to parse: {}".format(lines_parsed, lines_failed_parse))
		if (len(vect_fail_synch) > 0): print("Chromosomes that Failed to synch.: {}".format(",".join(vect_fail_synch)))
		self.utils.remove_dir(temp_work_dir)

	def parse_vcf(self, vcf_file_to_parse, vect_pass_ref):
		"""
		:param vcf_file_to_parse file VCF to parse
		:param vect_pass_ref = vector with chromosomes names to not procesee 
		Set new info in VCF file with hit position, tag=HIT_POS
		Info add: HIT_POS
		"""
		print("Start processing {} -> {}".format(self.reference_1.get_reference_name(),\
					self.reference_2.get_reference_name()))

		temp_work_dir = self.utils.get_temp_dir()		
		impose_minimap2_only = False
		lift_over_ligth = LiftOverLight(self.reference_1, self.reference_2, temp_work_dir, impose_minimap2_only, False)
		
		read_vcf = VcfProcess(vcf_file_to_parse, -1)
		(lines_parsed, lines_failed_parse, vect_fail_synch) = read_vcf.parse_vcf(self.outfile, vect_pass_ref, lift_over_ligth)
		
		print("Lines parsed: {}   Lines Failed to parse: {}".format(lines_parsed, lines_failed_parse))
		if (len(vect_fail_synch) > 0): print("Chromosomes that Failed to synch.: {}".format(",".join(vect_fail_synch)))
		self.utils.remove_dir(temp_work_dir)



