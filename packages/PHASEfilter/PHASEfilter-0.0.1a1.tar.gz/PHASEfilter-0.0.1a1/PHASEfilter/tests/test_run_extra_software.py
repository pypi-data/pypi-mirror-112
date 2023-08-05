'''
Created on 01/06/2020

@author: mmp
'''
import unittest, os
from PHASEfilter.lib.utils.run_extra_software import RunExtraSoftware
from PHASEfilter.lib.utils.util import Utils

class Test(unittest.TestCase):

	utils = Utils()
	run_extra_software = RunExtraSoftware()
	
	def test_vcf_empty_name(self):
		
		vcf_file_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/vcf/test_tabix.vcf")
		self.assertTrue(os.path.exists(vcf_file_name))
		
		temp_dir = self.utils.get_temp_dir()
		chr_name = 'Chr Not found'
		(temp_out_vcf, number_of_records) = self.run_extra_software.get_vcf_with_only_chr(vcf_file_name, chr_name, temp_dir)
		self.assertEqual(0, number_of_records)
		self.assertTrue(temp_out_vcf is None)
		
	def test_run_extra_software(self):
		
		vcf_file_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/vcf/test_tabix.vcf")
		self.assertTrue(os.path.exists(vcf_file_name))
		
		temp_file_name_bgz = self.utils.get_temp_file("temp_file_", ".vcf.gz")
		self.run_extra_software.make_bgz(vcf_file_name, temp_file_name_bgz)
		self.assertTrue(os.path.exists(temp_file_name_bgz))
		self.assertTrue(os.path.getsize(temp_file_name_bgz) > 200)
		
		temp_file_name = self.utils.get_temp_file("temp_file_", ".vcf")
		self.run_extra_software.make_unzip_bgz(temp_file_name_bgz, temp_file_name)
		self.assertTrue(os.path.exists(temp_file_name))
		self.assertTrue(os.path.getsize(vcf_file_name) == os.path.getsize(temp_file_name))
		
		self.utils.remove_file(temp_file_name_bgz)
		self.utils.remove_file(temp_file_name)

if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.test_run_extra_software']
	unittest.main()