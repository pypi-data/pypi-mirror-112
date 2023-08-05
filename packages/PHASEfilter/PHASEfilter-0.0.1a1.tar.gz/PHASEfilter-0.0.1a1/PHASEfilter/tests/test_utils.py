'''
Created on 13/05/2020

@author: mmp
'''
import unittest, os
from PHASEfilter.lib.utils.util import Utils, NucleotideCodes
from PHASEfilter.lib.utils.reference import Reference
from PHASEfilter.lib.utils.run_extra_software import RunExtraSoftware

class Test(unittest.TestCase):


	def setUp(self):
		pass


	def tearDown(self):
		pass

	def test_refernce_names(self):
		ref_1 = Reference()
		ref_1.vect_reference = ['aaaa', 'aaba', 'aaca']
		ref_2 = Reference()
		ref_2.vect_reference = ['aaaa', 'aaba', 'aaca']

		self.assertEqual('aaaa', ref_1.get_chr_in_genome('aaaa'))
		self.assertEqual('aaba', ref_1.get_chr_in_genome('aaba'))

		ref_1.vect_reference = ['Ca22chr1A_C_albicans_SC5314', 'aaba', 'aaca']
		ref_2.vect_reference = ['Ca22chr1B_C_albicans_SC5314', 'aaba', 'aaca']
		self.assertEqual('Ca22chr1B_C_albicans_SC5314', ref_2.get_chr_in_genome('Ca22chr1A_C_albicans_SC5314'))


	def test_tabix(self):
		utils = Utils()
		run_extra_software = RunExtraSoftware()
		
		vcf_file_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/vcf/test_tabix.vcf")
		self.assertTrue(os.path.exists(vcf_file_name))
		
		temp_dir = utils.get_temp_dir()
		chr_name = 'Ca22chr1A_C_albicans_SC5314'
		(temp_out_vcf, number_of_records) = run_extra_software.get_vcf_with_only_chr(vcf_file_name, chr_name, temp_dir)
		
		self.assertEqual(2209, number_of_records)
		vect_out = run_extra_software.vcf_lines_for_position(temp_out_vcf, chr_name, 1768, 1769)
		self.assertEqual(1, len(vect_out))
		self.assertTrue(vect_out[0].startswith("Ca22chr1A_C_albicans_SC5314	1768"))
		
		vect_out = run_extra_software.vcf_lines_for_position(temp_out_vcf, chr_name, 1768, 1768)
		self.assertEqual(1, len(vect_out))
		self.assertTrue(vect_out[0].startswith("Ca22chr1A_C_albicans_SC5314	1768"))

		vect_out = run_extra_software.vcf_lines_for_position(temp_out_vcf, chr_name, 1971, 1972)
		self.assertEqual(2, len(vect_out))

		chr_name = 'Ca22chrRA_C_albicans_SC5314'
		vect_out = run_extra_software.vcf_lines_for_position(temp_out_vcf, chr_name, 1813312, 1813313)
		self.assertEqual(0, len(vect_out))
		
		chr_name = 'Ca22chrRA_C_albicans_SC5314___'
		(temp_out_vcf_2, number_of_records) = run_extra_software.get_vcf_with_only_chr(vcf_file_name, chr_name, temp_dir)
		self.assertEqual(None, temp_out_vcf_2)
		self.assertEqual(0, number_of_records)
		
		## remove dir
		utils.remove_dir(temp_dir)
		utils.remove_file(temp_out_vcf)
		utils.remove_file(temp_out_vcf + ".tbi")

	def test_tabix_2(self):
		utils = Utils()
		run_extra_software = RunExtraSoftware()
		
		vcf_file_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/vcf/test_tabix.vcf")
		self.assertTrue(os.path.exists(vcf_file_name))
		
		temp_dir = utils.get_temp_dir()
		chr_name = 'Ca22chrRA_C_albicans_SC5314'
		(temp_out_vcf, number_of_records) = run_extra_software.get_vcf_with_only_chr(vcf_file_name, chr_name, temp_dir)
		self.assertEqual(50, number_of_records)
		
		vect_out = run_extra_software.vcf_lines_for_position(temp_out_vcf, chr_name, 1813312, 1813313)
		self.assertEqual(1, len(vect_out))
		self.assertTrue(vect_out[0].startswith("Ca22chrRA_C_albicans_SC5314	1813312"))
		
		vect_out = run_extra_software.vcf_lines_for_position(temp_out_vcf, chr_name, 1813312, 1882546)
		self.assertEqual(2, len(vect_out))
		self.assertTrue(vect_out[0].startswith("Ca22chrRA_C_albicans_SC5314	1813312"))
		self.assertTrue(vect_out[1].startswith("Ca22chrRA_C_albicans_SC5314	1882546"))
		
		chr_name = 'Ca22chr1A_C_albicans_SC5314'
		vect_out = run_extra_software.vcf_lines_for_position(temp_out_vcf, chr_name, 1768, 1769)
		self.assertEqual(0, len(vect_out))
		
		## remove dir
		utils.remove_dir(temp_dir)
		utils.remove_file(temp_out_vcf)
		utils.remove_file(temp_out_vcf + ".tbi")

	def test_reference_bases(self):
		
		nucleotide_codes = NucleotideCodes()
		self.assertTrue(nucleotide_codes.has_this_base('W', 'A')) 
		self.assertTrue(nucleotide_codes.has_this_base('w', 'a')) 
		self.assertFalse(nucleotide_codes.has_this_base('w', 'c'))
		self.assertTrue(nucleotide_codes.has_this_base('R', 'a'))
		self.assertTrue(nucleotide_codes.has_this_base('R', 'G'))
		self.assertFalse(nucleotide_codes.has_this_base('R', 'u'))
		
		self.assertTrue(nucleotide_codes.has_this_base('Y', 'c'))
		self.assertTrue(nucleotide_codes.has_this_base('Y', 't'))
		self.assertFalse(nucleotide_codes.has_this_base('Y', 'a'))
		
if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.test_refernce_names']
	unittest.main()



