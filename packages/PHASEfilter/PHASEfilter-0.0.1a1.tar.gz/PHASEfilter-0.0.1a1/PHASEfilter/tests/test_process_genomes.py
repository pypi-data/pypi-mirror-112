'''
Created on 01/06/2020

@author: mmp
'''
import unittest, os
from PHASEfilter.lib.utils.util import Utils
from PHASEfilter.lib.process.process_genomes import ProcessTwoGenomes

class Test(unittest.TestCase):

	utils = Utils()
	
	def test_process_chromosome(self):
		"""
		"""
		
		seq_file_name_a = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/ref/ref_ca22_1A.fasta")
		seq_file_name_b = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/ref/ref_ca22_1B.fasta")
		self.assertTrue(os.path.exists(seq_file_name_a))
		self.assertTrue(os.path.exists(seq_file_name_b))
		
		vcf_1 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/vcf/chrA.vcf")
		vcf_2 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/vcf/chrB.vcf")
		
		outfile_vcf = self.utils.get_temp_file("dont_care_", ".vcf")
		outfile_vcf_removed = self.utils.get_temp_file("dont_care_2", ".vcf")
		report_out_temp = self.utils.get_temp_file("report_temp_", ".txt")
		threshold_ad = 0.01
		process_two_genomes = ProcessTwoGenomes(seq_file_name_a, seq_file_name_b, vcf_1, vcf_2, threshold_ad, outfile_vcf)

		chr_name_A = "Ca22chr1A_C_albicans_SC5314"
		chr_name_B = "Ca22chr1B_C_albicans_SC5314"
		print_results = False
		self.assertEqual((True, True), process_two_genomes.process_chromosome(chr_name_A, chr_name_B, outfile_vcf, outfile_vcf_removed, report_out_temp, print_results))

		vect_data = self.utils.read_text_file(report_out_temp)
		self.assertEqual(1, len(vect_data))
		self.assertEqual("8	115	0	2078	8	2209	2201	minimap2	100.00", vect_data[0])
		self.assertTrue(os.path.getsize(outfile_vcf) > 200)
		
		## remove files
		self.utils.remove_file(report_out_temp)
		self.utils.remove_file(outfile_vcf)
		self.utils.remove_file(outfile_vcf_removed)

	def test_process_chromosome_1(self):
		"""
		"""
		
		seq_file_name_a = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/ref/ref_ca22_1A_multiple.fasta")
		seq_file_name_b = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/ref/ref_ca22_1B_multiple.fasta")
		self.assertTrue(os.path.exists(seq_file_name_a))
		self.assertTrue(os.path.exists(seq_file_name_b))
		
		vcf_1 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/vcf/chrA.vcf")
		vcf_2 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/vcf/chrB.vcf")
		
		outfile_vcf = self.utils.get_temp_file("dont_care_", ".vcf")
		outfile_vcf_removed = self.utils.get_temp_file("dont_care_2", ".vcf")
		report_out_temp = self.utils.get_temp_file("report_temp_", ".txt")
		threshold_ad = 0.01
		process_two_genomes = ProcessTwoGenomes(seq_file_name_a, seq_file_name_b, vcf_1, vcf_2, threshold_ad, outfile_vcf)

		chr_name_A = "Ca22chr1A_C_albicans_SC5314"
		chr_name_B = "Ca22chr2B_C_albicans_SC5314"
		print_results = False
		self.assertEqual((True, False), process_two_genomes.process_chromosome(chr_name_A, chr_name_B, outfile_vcf, outfile_vcf_removed, report_out_temp, print_results))

		vect_data = self.utils.read_text_file(report_out_temp)
		self.assertEqual(1, len(vect_data))
		self.assertEqual("0	2209	0	0	0	0	2209	minimap2	60.28", vect_data[0])
		self.assertTrue(os.path.getsize(outfile_vcf) > 200)
		
		## remove files
		self.utils.remove_file(report_out_temp)
		self.utils.remove_file(outfile_vcf)
		self.utils.remove_file(outfile_vcf_removed)
		
	def test_process_chromosome_2(self):
		"""
		"""
		
		seq_file_name_a = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/ref/ref_ca22_1A_multiple.fasta")
		seq_file_name_b = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/ref/ref_ca22_1B_multiple.fasta")
		self.assertTrue(os.path.exists(seq_file_name_a))
		self.assertTrue(os.path.exists(seq_file_name_b))
		
		vcf_1 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/vcf/chrA.vcf")
		vcf_2 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/vcf/chrB.vcf")
		
		outfile_vcf = self.utils.get_temp_file("dont_care_", ".vcf")
		outfile_vcf_removed = self.utils.get_temp_file("dont_care_2", ".vcf")
		report_out_temp = self.utils.get_temp_file("report_temp_", ".txt")
		threshold_ad = 0.01
		process_two_genomes = ProcessTwoGenomes(seq_file_name_a, seq_file_name_b, vcf_1, vcf_2, threshold_ad, outfile_vcf)

		chr_name_A = "Ca22chr2A_C_albicans_SC5314"
		chr_name_B = "Ca22chr1B_C_albicans_SC5314"
		print_results = False
		self.assertEqual((False, False), process_two_genomes.process_chromosome(chr_name_A, chr_name_B, outfile_vcf, outfile_vcf_removed, report_out_temp, print_results))

		vect_data = self.utils.read_text_file(report_out_temp)
		self.assertEqual(1, len(vect_data))
		self.assertEqual("0	0	0	0	0	0	0	minimap2	55.01", vect_data[0])
		self.assertEqual(0, os.path.getsize(outfile_vcf))
		
		## remove files
		self.utils.remove_file(report_out_temp)
		self.utils.remove_file(outfile_vcf)
		self.utils.remove_file(outfile_vcf_removed)
		
	def test_process_chromosome_3(self):
		"""
		"""
		
		seq_file_name_a = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/ref/ref_ca22_1A_multiple.fasta")
		seq_file_name_b = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/ref/ref_ca22_1B_multiple.fasta")
		self.assertTrue(os.path.exists(seq_file_name_a))
		self.assertTrue(os.path.exists(seq_file_name_b))
		
		vcf_1 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/vcf/chrA.vcf")
		vcf_2 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/vcf/chrB.vcf")
		
		outfile_vcf = self.utils.get_temp_file("dont_care_", ".vcf")
		outfile_vcf_removed = self.utils.get_temp_file("dont_care_2", ".vcf")
		report_out_temp = self.utils.get_temp_file("report_temp_", ".txt")
		threshold_ad = 0.01
		process_two_genomes = ProcessTwoGenomes(seq_file_name_a, seq_file_name_b, vcf_1, vcf_2, threshold_ad, outfile_vcf)

		chr_name_A = "Ca22chr2A_C_albicans_SC5314"
		chr_name_B = "Ca22chr2B_C_albicans_SC5314"
		print_results = False
		self.assertEqual((False, False), process_two_genomes.process_chromosome(chr_name_A, chr_name_B, outfile_vcf, outfile_vcf_removed, report_out_temp, print_results))

		vect_data = self.utils.read_text_file(report_out_temp)
		self.assertEqual(1, len(vect_data))
		self.assertEqual("0	0	0	0	0	0	0	minimap2	93.58", vect_data[0])
		self.assertEqual(0, os.path.getsize(outfile_vcf))
		
		## remove files
		self.utils.remove_file(report_out_temp)
		self.utils.remove_file(outfile_vcf)
		self.utils.remove_file(outfile_vcf_removed)

if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.test_process_chromosome']
	unittest.main()