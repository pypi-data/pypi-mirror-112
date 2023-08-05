'''
Created on 27/05/2020

@author: mmp
'''
import os, vcf
from PHASEfilter.lib.utils.software import Software
from PHASEfilter.lib.utils.util import Utils

class RunExtraSoftware(object):
	'''
	classdocs
	'''

	software = Software()
	utils = Utils()
	
	def __init__(self):
		'''
		Constructor
		'''
		pass
	
	def make_tabix(self, vcf_file):
		"""
		create a index for vcf.gz file
		"""
		if (vcf_file is None): return
		if (not os.path.exists(vcf_file + ".tbi")):
			cmd = "{} {} -p vcf".format(self.software.get_tabix(), vcf_file)
			exist_status = os.system(cmd)
			if (exist_status != 0):
				raise Exception("Fail to run tabix.\n{}".format(cmd))
		
	def make_bgz(self, file_name, file_name_bgz):
		"""
		create a bgz file
		"""
		cmd = "{} -c {} > {}".format(self.software.get_bgzip(), file_name, file_name_bgz)
		exist_status = os.system(cmd)
		if (exist_status != 0):
			raise Exception("Fail to run bgzip.\n{}".format(cmd))
		self.make_tabix(file_name_bgz)
	
	def make_unzip_bgz(self, file_name_bgz, file_name):
		"""
		create a bgz file
		"""
		cmd = "{} -cd {} > {}".format(self.software.get_bgzip(), file_name_bgz, file_name)
		exist_status = os.system(cmd)
		if (exist_status != 0):
			raise Exception("Fail to run bgzip.\n{}".format(cmd))
			
	def get_vcf_with_only_chr(self, vcf_file, chr_name, temp_work_dir):
		"""
		:param vcf file in
		:param chr to filter
		:param tmp directory where is possible to create temp files, remove after
		:out return (vcf file with only this chr name, None if there's no records for this VCF chr name,
				number_of_variants -> number of variants in new file)
		"""
		
		temp_vcf_file = self.utils.get_temp_file(chr_name.replace(' ', ''), ".vcf.gz")
		
		if (vcf_file.endswith(".vcf")):
			vcf_file_temp = self.utils.get_temp_file_with_path(temp_work_dir, "tmp_vcf", ".vcf.gz")
			cmd = "{} -c {} > {}".format(self.software.get_bgzip(), vcf_file, vcf_file_temp)
			exist_status = os.system(cmd)
			if (exist_status != 0):
				raise Exception("Fail to run bgzip.\n{}".format(cmd))
			self.make_tabix(vcf_file_temp)
			vcf_file = vcf_file_temp
			
		# bcftools filter xpto.vcf.gz -r 4 | gzip -c - > 
		self.make_tabix(vcf_file)
		cmd = "{} filter {} -r {} | {} -c > {}".format(self.software.get_bcf_tools(), vcf_file,\
						chr_name, self.software.get_bgzip(), temp_vcf_file)
		exist_status = os.system(cmd)
		if (exist_status != 0):
			raise Exception("Fail to run bcftools.\n{}".format(cmd))
		
		### test VCF if has fields
		with open(temp_vcf_file, 'rb') as handle_in:
			vcf_reader = vcf.Reader(handle_in, compressed=True)
			for _ in vcf_reader:
				## create index
				self.make_tabix(temp_vcf_file)
				
				number_of_variants = self.get_variant_number_vcf_file(temp_vcf_file)
				return (temp_vcf_file, number_of_variants)
		
		### returns empty file if there's no variants for a specific chromosome
		self.utils.remove_file(temp_vcf_file)
		return (None, 0)

				
	def get_variant_number_vcf_file(self, vcf_file):
		"""
		:out number of variations in vcf file
		"""
		temp_stats_txt = self.utils.get_temp_file("stats", ".txt")
		cmd = "{} stats {} > {}".format(self.software.get_bcf_tools(), vcf_file,\
				temp_stats_txt)
		exist_status = os.system(cmd)
		if (exist_status != 0):
			raise Exception("Fail to run bcftools.\n{}".format(cmd))
		
		### read data
		vect_data = self.utils.read_text_file(temp_stats_txt)
		
		### remove file
		self.utils.remove_file(temp_stats_txt)
		
		for line in vect_data:
			if (line.find('number of records:') != -1):
				lst_data = line.split()
				if (self.utils.is_integer(lst_data[5])): return int(lst_data[5])
				return 0
		return 0

	
	def concat_vcf(self, temp_work_dir, prefix, extention, outfile_vcf):
		"""
		merge several output files
		/usr/bin/bcftools merge Home/data/*vcf.gz -Oz -o Merged.vcf.gz
		"""
		cmd = "{} concat -Oz -o {} {}".format(self.software.get_bcf_tools(), outfile_vcf,\
				os.path.join(temp_work_dir, "{}*{}".format(prefix, extention)))
		exist_status = os.system(cmd)
		if (exist_status != 0):
			raise Exception("Fail to run bcftools.\n{}".format(cmd))


	def vcf_lines_for_position(self, vcf_file_name, chr_name, start, end, file_to_write = None):
		"""
		:param vcf source file_name 
		:param chr_name to filter 
		:param start
		:param end
		:out array with vcf output, empty value if exist file to save
		"""
		if (not file_to_write is None): temp_file = file_to_write
		else: temp_file = self.utils.get_temp_file("out_vcf", ".vcf")
		cmd = "{} {} -p vcf {}:{}-{} >> {}".format(self.software.get_tabix(),\
					vcf_file_name, chr_name, start, end, temp_file)
		exist_status = os.system(cmd)
		if (exist_status != 0):
			raise Exception("Fail to run tabix.\n{}".format(cmd))
		
		if (file_to_write is None):
			vect_out = self.utils.read_text_file(temp_file)
			self.utils.remove_file(temp_file)
			self.utils.remove_file(temp_file + ".tbi")
			return vect_out
		return []

