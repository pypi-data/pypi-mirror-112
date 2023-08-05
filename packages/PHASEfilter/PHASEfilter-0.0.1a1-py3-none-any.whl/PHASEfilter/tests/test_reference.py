'''
Created on 20/05/2020

@author: mmp
'''
import unittest, os
from PHASEfilter.lib.utils.util import Utils
from PHASEfilter.lib.utils.reference import Reference, Bases

class Test(unittest.TestCase):

	utils = Utils()
	
	def test_reference(self):
		
		seq_file_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/ref/ref_ca22_1A.fasta")
		self.assertTrue(os.path.exists(seq_file_name))
		
		reference = Reference(seq_file_name)
		temp_file = self.utils.get_temp_file("result_fasta", ".txt")
		self.assertEqual("G", reference.get_base_in_position("Ca22chr1A_C_albicans_SC5314", 1, 1, temp_file))
		self.assertEqual("A", reference.get_base_in_position("Ca22chr1A_C_albicans_SC5314", 71, 71, temp_file))
		self.assertEqual("G", reference.get_base_in_position("Ca22chr1A_C_albicans_SC5314", 141, 141, temp_file))
		self.assertEqual("GC", reference.get_base_in_position("Ca22chr1A_C_albicans_SC5314", 141, 142, temp_file))
		self.assertEqual("GCGGTTAGACATACGTGATATTCACCGACTTTGAGAGTCCCACTAATCGGCTAGACATACGTAAATTACATAGCTCCCTCCAATACACACCCTACTTACTAT",\
			reference.get_base_in_position("Ca22chr1A_C_albicans_SC5314", 141, 242, temp_file))
		self.utils.remove_file(temp_file)

		### chr length
		self.assertEqual(69930, reference.get_chr_length("Ca22chr1A_C_albicans_SC5314"))
		
		self.assertEqual("Ca22chr1A_C_albicans_SC5314", reference.get_chr_in_genome("Ca22chr1A_C_albicans_SC5314"))
		
	def test_count_data(self):
		
		bases = Bases()
		bases.count_bases("AAACCCGGGTTTWWWWSSSVVn")
		self.assertEqual("A\tC\tG\tT\tU\tR\tY\tS\tW\tK\tM\tB\tD\tH\tV\tN", bases.get_header()) 
		self.assertEqual("3\t3\t3\t3\t0\t0\t0\t3\t4\t0\t0\t0\t0\t0\t2\t1", str(bases))
		
		bases_sum = Bases()
		bases_sum += bases
		self.assertEqual("3\t3\t3\t3\t0\t0\t0\t3\t4\t0\t0\t0\t0\t0\t2\t1", str(bases_sum))
		bases_sum += bases
		self.assertEqual("6\t6\t6\t6\t0\t0\t0\t6\t8\t0\t0\t0\t0\t0\t4\t2", str(bases_sum))


	def test_count_in_reference(self):
		
		seq_file_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/ref/ref_ca22_1A.fasta")
		self.assertTrue(os.path.exists(seq_file_name))
		
		ref_count_result = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/result/count_ref_ca22_1A.txt")
		self.assertTrue(os.path.exists(ref_count_result))
		temp_file = self.utils.get_temp_file("result_fasta", ".txt")
		
		reference = Reference(seq_file_name)
		reference.count_bases()
		reference.save_count_bases_in_file(temp_file)
		
		vect_result_obtanied = self.utils.read_text_file(ref_count_result)
		vect_result_expected = self.utils.read_text_file(temp_file)
		for _ in range(len(vect_result_obtanied)):
			self.assertEqual(vect_result_obtanied[_], vect_result_expected[_])
		self.utils.remove_file(temp_file)
	
	def test_name(self):
		
		seq_file_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/referenceSaccharo/S01.fa")
		self.assertTrue(os.path.exists(seq_file_name))
		
		reference = Reference(seq_file_name)
		self.assertEqual("chrI", reference.get_chr_in_genome("chrI"))
		self.assertEqual("chrII", reference.get_chr_in_genome("chrII"))
		
		try:
			self.assertEqual("", reference.get_chr_in_genome("chr"))
			self.fail("Must throw exception")
		except:
			pass
		
	def test_name_2(self):
		
		seq_file_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/referenceSaccharo/ref_ony_for_names.fasta")
		self.assertTrue(os.path.exists(seq_file_name))
		
		reference = Reference(seq_file_name)
		self.assertEqual("chrI", reference.get_chr_in_genome("chrI"))
		self.assertEqual("chrII", reference.get_chr_in_genome("chrII"))
		try:
			self.assertEqual("chrII", reference.get_chr_in_genome("chrmt"))
		except Exception as e:
			self.assertEqual(str(e), "Error: there are more than one candidate for this chr 'chrmt' -> ['chrMT.1', 'chrMT.2']" +\
							"\nYou can not process this chr 'chrmt' passing the follow paramateres in CLI '--pass_ref chrmt'")
		
		try:
			self.assertEqual("", reference.get_chr_in_genome("chr"))
			self.fail("Must throw exception")
		except:
			pass
		
if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.test_reference']
	unittest.main()