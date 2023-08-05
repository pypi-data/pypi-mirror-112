'''
Created on 06/12/2019

@author: mmp
'''
from PHASEfilter.lib.utils.util import Utils
from PHASEfilter.lib.utils.reference import Reference
from PHASEfilter.lib.utils.vcf_process import VcfProcess, CountAlleles
from PHASEfilter.lib.utils.lift_over_simple import LiftOverLight
from PHASEfilter.lib.utils.run_extra_software import RunExtraSoftware
import os

class ProcessTwoGenomes(object):
	
	utils = Utils("synchronize")
	run_extra_software = RunExtraSoftware()
	
	def __init__(self, reference_1, reference_2, vcf_1, vcf_2, threshold_heterozygous_ad, outfile_vcf):
		"""
		set the data
		"""
		### read references
		self.reference_1 = Reference(reference_1)
		self.reference_2 = Reference(reference_2)
		self.vcf_1 = vcf_1
		self.vcf_2 = vcf_2
		self.outfile_vcf = outfile_vcf
		self.threshold_heterozygous_ad = threshold_heterozygous_ad
	
	def get_report_file(self):
		"""
		:out get file name where report will be saved
		"""
		return os.path.join(os.path.dirname(self.outfile_vcf),\
			"{}_{}".format(self.utils.get_file_name_without_extension(self.outfile_vcf).replace('.vcf', ''),\
			"report.txt"))

	def get_vcf_removed_file(self):
		"""
		:out get file name where report will be saved
		"""
		return os.path.join(os.path.dirname(self.outfile_vcf),\
			"{}_{}".format(self.utils.get_file_name_without_extension(self.outfile_vcf).replace('.vcf', ''),\
			"removed.vcf.gz"))

	
	def process(self):
		"""
		save one VCF with Heterozygous SNPs remove, from 1 to 2 
		"""
		print("\nStart processing....")
		print_results = False
				
		### variables to temp output vcf file
		extension_out = ".vcf"
		prefix = "vcf_out"
		
		### Process one chr at time 
		vect_process_B = []
		vect_not_process_A = []
		vect_temp_report_file = []		### at the end merge all of them
		temp_work_dir = self.utils.get_temp_dir()
		temp_work_dir_vcf_removed = self.utils.get_temp_dir()
		for chr_name_A in self.reference_1.vect_reference:
			chr_name_B = self.reference_2.get_chr_in_genome(chr_name_A)
			if chr_name_B is None: 
				vect_not_process_A.append(chr_name_A)
				continue
			vect_process_B.append(chr_name_B)
			
			vcf_out_temp = self.utils.get_temp_file_with_path(temp_work_dir, prefix, extension_out)
			vcf_out_removed_temp = self.utils.get_temp_file_with_path(temp_work_dir_vcf_removed, prefix, extension_out)
			vcf_out_LOH_temp = self.utils.get_temp_file_with_path(temp_work_dir_vcf_removed, prefix, extension_out)
			report_out_temp = self.utils.get_temp_file_with_path(temp_work_dir, "report_out", ".txt")
			
			### processing chromosomes
			vect_temp_report_file.append([chr_name_A, chr_name_B, report_out_temp])
			(has_vcf_results, has_vcf_removed_results) = self.process_chromosome(chr_name_A, chr_name_B, vcf_out_temp,
															vcf_out_removed_temp, vcf_out_LOH_temp, report_out_temp,
															print_results)

			### test if has results
			if (has_vcf_results):			
				### make gzip file
				self.run_extra_software.make_bgz(vcf_out_temp, vcf_out_temp + ".gz")
			else:
				self.utils.remove_file(vcf_out_temp)
				
			### test if has removed results
			if (has_vcf_removed_results):			
				### make gzip file
				self.run_extra_software.make_bgz(vcf_out_removed_temp, vcf_out_removed_temp + ".gz")
			else:
				self.utils.remove_file(vcf_out_removed_temp)			
		
		### join report files
		with open(self.get_report_file(), 'w') as handle_write:
			count_alleles = CountAlleles()
			handle_write.write("Source genome\t{}\nHit genome\t{}\n\nSource genome\tHit genome\nChromosomes\tChromosomes\t".format(\
					self.reference_1.get_reference_name(),\
					self.reference_2.get_reference_name())\
					+ count_alleles.get_header() + "\tMethod\tAlignment %\n")
			count_alleles = CountAlleles()
			for vect_data in vect_temp_report_file:
				for line in self.utils.read_text_file(vect_data[2]):
					count_alleles.add_line(line.strip())
					handle_write.write("{}\t{}\t{}\n".format(vect_data[0], vect_data[1], line))
			handle_write.write("Total\t\t{}\n".format(str(count_alleles)))
			
		### join vcf output files
		self.run_extra_software.concat_vcf(temp_work_dir, prefix, extension_out + ".gz", self.outfile_vcf)
		self.run_extra_software.concat_vcf(temp_work_dir_vcf_removed, prefix, extension_out + ".gz", self.get_vcf_removed_file())
		
		### print chr not process
		vect_not_processed_B = self.reference_2.chr_not_included(vect_process_B)
		vect_not_processed_A = vect_not_process_A
		if (len(vect_not_processed_A) == 0): print("All chromosomes are processed for genome 1")
		else: print("Warning: chromosomes not processed for {}: ['{}']".format(self.reference_1.get_reference_name(), "', '".join(vect_not_processed_A)))
		if (len(vect_not_processed_B) == 0): print("All chromosomes are processed for genome 2")
		else: print("Warning: chromosomes not processed for {}: ['{}']".format(self.reference_2.get_reference_name(), "', '".join(vect_not_processed_B)))
	
		### remove temp files
#		self.utils.remove_dir(temp_work_dir)
#		self.utils.remove_dir(temp_work_dir_vcf_removed)
			
		### print info
		print("VCF result: {}".format(self.outfile_vcf))
		print("VCF removed variants result: {}".format(self.get_vcf_removed_file()))
		print("Report result: {}".format(self.get_report_file()))
	
	
	def process_chromosome(self, chr_name_A, chr_name_B, vcf_out_temp, vcf_out_removed_temp, vcf_out_LOH_temp,
						report_out_temp, print_results = True):
		"""
		process by chromosome
		:out has vcf result file
		"""
		print("*" * 50 + "\n" + "*" * 50 + "\nStart processing {} chr: {} ->  {} chr: {}".format(self.reference_1.get_reference_name(),\
					chr_name_A, self.reference_2.get_reference_name(), chr_name_B))
		temp_work_dir = self.utils.get_temp_dir()
		
		lift_over_ligth = LiftOverLight(self.reference_1, self.reference_2, temp_work_dir)
		lift_over_ligth.synchronize_sequences(chr_name_A, chr_name_B)
		
		### get only vcf sequences from chr_name_A
		(vcf_1_only_chr, number_of_records_1) = self.run_extra_software.get_vcf_with_only_chr(self.vcf_1, chr_name_A, temp_work_dir)
		(vcf_2_only_chr, number_of_records_2) = self.run_extra_software.get_vcf_with_only_chr(self.vcf_2, chr_name_B, temp_work_dir)
		
		## all VCF files has variants
		has_result_file = False
		has_vcf_removed_results = False
		if (not vcf_1_only_chr is None and not vcf_2_only_chr is None):
			### start processing VCF
			vcf_process = VcfProcess(vcf_1_only_chr, self.threshold_heterozygous_ad, print_results)
			vcf_process.match_vcf_to(chr_name_A, lift_over_ligth, vcf_2_only_chr, chr_name_B,
						vcf_out_temp, vcf_out_removed_temp, vcf_out_LOH_temp)
			
			count_alleles = vcf_process.count_alleles
			if (count_alleles.has_saved_variants()): has_result_file = True
			if (count_alleles.has_removed_variants()): has_vcf_removed_results = True
		elif (vcf_1_only_chr is None):
			count_alleles = CountAlleles()
		elif (not vcf_1_only_chr is None and vcf_2_only_chr is None):
			count_alleles = CountAlleles()
			count_alleles.diff_allele = number_of_records_1
			count_alleles.add_allele(number_of_records_2)
			self.run_extra_software.make_unzip_bgz(vcf_1_only_chr, vcf_out_temp)
			has_result_file = True

		### write the report
		best_method = lift_over_ligth.get_method_best_method(chr_name_A, chr_name_B)
		with open(report_out_temp, 'w') as handle_write:
			handle_write.write(str(count_alleles) +\
					"\t{}\t{:.2f}\n".format(best_method,\
					lift_over_ligth.get_percent_alignment(best_method, chr_name_A, chr_name_B)))

			
		### remove temp files
		self.utils.remove_dir(temp_work_dir)
		self.utils.remove_file(vcf_1_only_chr)
		if (not vcf_1_only_chr is None): self.utils.remove_file(vcf_1_only_chr + ".tbi")
		self.utils.remove_file(vcf_2_only_chr)
		if (not vcf_2_only_chr is None): self.utils.remove_file(vcf_2_only_chr + ".tbi")
		print("Processed {} chr: {} ->  {} chr: {}".format(self.reference_1.get_reference_name(),\
					chr_name_A, self.reference_2.get_reference_name(), chr_name_B))
		return (has_result_file, has_vcf_removed_results)
		
		
	def _process_unique_chromosome(self, chr_name_A, vcf_out_temp, report_out_temp, print_results = True):
		"""
		testing only the bases in the main reference
		"""
		print("Start processing {} chr: {}".format(self.reference_1.get_reference_name(),\
					chr_name_A))
		temp_work_dir = self.utils.get_temp_dir()
		
		### get only vcf sequences from chr_name_A
		(vcf_1_only_chr, number_of_records) = self.run_extra_software.get_vcf_with_only_chr(self.vcf_1, chr_name_A, temp_work_dir)
		
		### start processing VCF
		vcf_process = VcfProcess(vcf_1_only_chr, self.threshold_ad, print_results)
		vcf_process.match_vcf_to_refence(chr_name_A, self.reference_1, vcf_out_temp)
		
		### write the report
		with open(report_out_temp, 'w') as handle_write:
			handle_write.write(str(vcf_process.count_alleles) + "\n")
			
		self.utils.remove_dir(temp_work_dir)
		self.utils.remove_file(vcf_1_only_chr)
		self.utils.remove_file(vcf_1_only_chr + ".tbi")
		print("Processed {} chr: {}".format(self.reference_1.get_reference_name(), chr_name_A))



