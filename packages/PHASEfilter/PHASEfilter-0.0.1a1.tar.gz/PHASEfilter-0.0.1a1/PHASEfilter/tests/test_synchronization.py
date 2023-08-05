'''
Created on 16/06/2020

@author: mmp
'''
import unittest, os
from PHASEfilter.lib.utils.util import Utils
from PHASEfilter.lib.utils.reference import Reference
from PHASEfilter.lib.utils.lift_over_simple import LiftOverLight
from PHASEfilter.lib.process.process_references import ProcessTwoReferences

class Test(unittest.TestCase):


	def test_to_remove(self):
		
		utils = Utils("synchronize")
		temp_work_dir = utils.get_temp_dir()
		
		seq_file_name_a = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files/referenceSaccharo/S01.chrXVI.fa')
		seq_file_name_b = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files/referenceSaccharo/S228C.chrXVI.fa')
		self.assertTrue(os.path.exists(seq_file_name_a))
		self.assertTrue(os.path.exists(seq_file_name_b))
		
		seq_name_a = "chrXVI"
		seq_name_b = "chrXVI"
		position = 10000
		
		reference_a = Reference(seq_file_name_a)
		reference_b = Reference(seq_file_name_b)
		impose_minimap2_only = False
		lift_over_ligth = LiftOverLight(reference_a, reference_b, temp_work_dir, impose_minimap2_only, True)
		lift_over_ligth.synchronize_sequences(seq_name_a, seq_name_b)
		self.assertEqual((10011, -1), lift_over_ligth.get_pos_in_target(seq_name_a, seq_name_b, position))

		temp_out = utils.get_temp_file("out_sync_saccharo", ".txt")
		process_two_references = ProcessTwoReferences(seq_file_name_a, seq_file_name_b, temp_out)
		process_two_references.process()
		
		out_result_expected = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files/referenceSaccharo/out_sync_saccharo.txt')
		
		temp_diff = utils.get_temp_file("diff_file", ".txt")
		cmd = "diff {} {} > {}".format(temp_out, out_result_expected, temp_diff)
		os.system(cmd)
		vect_result = utils.read_text_file(temp_diff)
		self.assertEqual(0, len(vect_result))
		
		utils.remove_file(temp_out)
		utils.remove_file(temp_diff)
		
if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.test_to_remove']
	unittest.main() 