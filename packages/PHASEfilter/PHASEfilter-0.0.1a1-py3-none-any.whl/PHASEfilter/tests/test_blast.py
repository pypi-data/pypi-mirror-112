'''
Created on 20/05/2020

@author: mmp
'''
import unittest, os
from PHASEfilter.lib.utils.blast_two_sequences import BlastTwoSequences, BlastDescritpion, BlastAlignment, SyncHoles
from PHASEfilter.lib.utils.reference import Reference
from PHASEfilter.lib.utils.util import Utils

class Test(unittest.TestCase):


	def test_parse_blast(self):
		
		use_multithreading = False
		seq_file_name_a = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/ref/ref_ca22_1A.fasta")
		seq_file_name_b = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/ref/ref_ca22_1B.fasta")
		self.assertTrue(os.path.exists(seq_file_name_a))
		self.assertTrue(os.path.exists(seq_file_name_b))
		
		debug = True
		blast_two_sequences = BlastTwoSequences(seq_file_name_a, seq_file_name_b, debug, use_multithreading)
		blast_alignments = blast_two_sequences.align_data()
		blast_alignments.print_all_alignments()
		self.assertEqual(["35780M1I7729M"], blast_alignments.get_cigar(0).get_vect_cigar_string())
		self.assertEqual(["132M"], blast_alignments.get_cigar(-2).get_vect_cigar_string())
		self.assertEqual(["1171M1I1215M1I23762M"], blast_alignments.get_cigar(-1).get_vect_cigar_string())
		self.assertEqual(3, blast_alignments.get_number_alignments())
		self.assertEqual("69789\t69792\t0", str(blast_alignments.get_cigar_count_elements()))
		
	def test_make_cigar(self):
		
		#### new test
		seq_a = "AAAAAAC-TAAAT"
		seq_b = "AAAAAACAT-AAT"
		cigar = ["7M1I3M1D1M"]
		
		use_multithreading = False
		debug = True
		bast_line = BlastAlignment(debug, use_multithreading)
		previous_begin = 13
		bast_line.add_query(previous_begin, seq_a, len(seq_a) + previous_begin)
		bast_line.add_subject(13, seq_b, 20)
		
		bast_line.make_cigar_string()
		self.assertEqual("AAAAAAC-TAAAT", bast_line.get_query_sequence())
		self.assertEqual("AAAAAACATAA-T", bast_line.get_subject_sequence())
		self.assertEqual(2, len(bast_line.synchronize.vect_data))
		self.assertTrue(SyncHoles(7, SyncHoles.QUERY) == bast_line.synchronize.vect_data[0])
		self.assertTrue(SyncHoles(11, SyncHoles.SUBJECT) == bast_line.synchronize.vect_data[-1])
		self.assertEqual(cigar, bast_line.get_cigar().get_vect_cigar_string())
		self.assertEqual((-1, -1), bast_line.get_position_from_2_to(3))
		self.assertEqual((-1, -1), bast_line.get_position_from_2_to(12))
		self.assertEqual((13, -1), bast_line.get_position_from_2_to(13))
		self.assertEqual((14, -1), bast_line.get_position_from_2_to(14))
		self.assertEqual((19, -1), bast_line.get_position_from_2_to(19))
		self.assertEqual((21, -1), bast_line.get_position_from_2_to(20))
		self.assertEqual((22, -1), bast_line.get_position_from_2_to(21))
		self.assertEqual((23, -1), bast_line.get_position_from_2_to(22))
		self.assertEqual((-1, 23), bast_line.get_position_from_2_to(23))
		self.assertEqual((24, -1), bast_line.get_position_from_2_to(24))
		self.assertEqual((-1, -1), bast_line.get_position_from_2_to(25))
		
		#### new test
		seq_a = "AAAAAAC-TAAAT"
		seq_b = "AAAAAACAT-CAT"
		cigar = ["7M1I3M1D1M"]
		
		use_multithreading = False
		debug = True
		bast_line = BlastAlignment(debug, use_multithreading)
		previous_begin = 13
		bast_line.add_query(previous_begin, seq_a, len(seq_a) + previous_begin)
		bast_line.add_subject(13, seq_b, 20)
		
		bast_line.make_cigar_string()
		
		self.assertEqual("AAAAAAC-TAAAT", bast_line.get_query_sequence())
		self.assertEqual("AAAAAACATCA-T", bast_line.get_subject_sequence())
		self.assertEqual(2, len(bast_line.synchronize.vect_data))
		self.assertTrue(SyncHoles(7, SyncHoles.QUERY) == bast_line.synchronize.vect_data[0])
		self.assertTrue(SyncHoles(11, SyncHoles.SUBJECT) == bast_line.synchronize.vect_data[-1])
		self.assertEqual(cigar, bast_line.get_cigar().get_vect_cigar_string())
		
		#### new test
		seq_a = "AAAAAACATAAAT"
		seq_b = "AAAAAACAG--AT"
		cigar = ["10M2D1M"]
		
		use_multithreading = False
		debug = True
		bast_line = BlastAlignment(debug, use_multithreading)
		previous_begin = 13
		bast_line.add_query(previous_begin, seq_a, len(seq_a) + previous_begin)
		bast_line.add_subject(13, seq_b, 20)
		
		bast_line.make_cigar_string()
		self.assertEqual("AAAAAACATAAAT", bast_line.get_query_sequence())
		self.assertEqual("AAAAAACAGA--T", bast_line.get_subject_sequence())
		self.assertEqual(2, len(bast_line.synchronize.vect_data))
		self.assertTrue(SyncHoles(10, SyncHoles.SUBJECT) == bast_line.synchronize.vect_data[0])
		self.assertTrue(SyncHoles(11, SyncHoles.SUBJECT) == bast_line.synchronize.vect_data[1])
		self.assertEqual(cigar, bast_line.get_cigar().get_vect_cigar_string())

		#### new test
		seq_a = "AAAAAACATAAAAT"
		seq_b = "AAAAAACAG--AAT"
		cigar = ["11M2D1M"]
		
		use_multithreading = False
		debug = True
		bast_line = BlastAlignment(debug, use_multithreading)
		previous_begin = 13
		bast_line.add_query(previous_begin, seq_a, len(seq_a) + previous_begin)
		bast_line.add_subject(13, seq_b, 20)
		
		bast_line.make_cigar_string()
		self.assertEqual("AAAAAACATAAAAT", bast_line.get_query_sequence())
		self.assertEqual("AAAAAACAGAA--T", bast_line.get_subject_sequence())
		self.assertEqual(2, len(bast_line.synchronize.vect_data))
		self.assertTrue(SyncHoles(11, SyncHoles.SUBJECT) == bast_line.synchronize.vect_data[0])
		self.assertTrue(SyncHoles(12, SyncHoles.SUBJECT) == bast_line.synchronize.vect_data[1])
		self.assertEqual(cigar, bast_line.get_cigar().get_vect_cigar_string())
		
		#### new test
		seq_a = "AAAAAAC-TACAT"
		seq_b = "AAAAAACAG--AT"
		cigar = ["7M1I2M2D1M"]
		
		use_multithreading = False
		debug = True
		bast_line = BlastAlignment(debug, use_multithreading)
		previous_begin = 13
		bast_line.add_query(previous_begin, seq_a, len(seq_a) + previous_begin)
		bast_line.add_subject(13, seq_b, 20)
		
		bast_line.make_cigar_string()
		self.assertEqual("AAAAAAC-TACAT", bast_line.get_query_sequence())
		self.assertEqual("AAAAAACAGA--T", bast_line.get_subject_sequence())
		self.assertEqual(3, len(bast_line.synchronize.vect_data))
		self.assertTrue(SyncHoles(7, SyncHoles.QUERY) == bast_line.synchronize.vect_data[0])
		self.assertTrue(SyncHoles(10, SyncHoles.SUBJECT) == bast_line.synchronize.vect_data[1])
		self.assertTrue(SyncHoles(11, SyncHoles.SUBJECT) == bast_line.synchronize.vect_data[2])
		self.assertEqual(cigar, bast_line.get_cigar().get_vect_cigar_string())
		self.assertEqual((19, -1), bast_line.get_position_from_2_to(19))
		self.assertEqual((21, -1), bast_line.get_position_from_2_to(20))
		self.assertEqual((22, -1), bast_line.get_position_from_2_to(21))
		self.assertEqual((-1, 22), bast_line.get_position_from_2_to(22))
		self.assertEqual((-1, 22), bast_line.get_position_from_2_to(23))
		self.assertEqual((23, -1), bast_line.get_position_from_2_to(24))
		self.assertEqual((-1, -1), bast_line.get_position_from_2_to(25))
		
		
		#### new test
		seq_a = "AAAAAAC---ATACAAAAT"
		seq_b = "AAAAAACAAAATA----AT"
		cigar = ["8M3I2M1D1M3D1M"]
		
		use_multithreading = False
		debug = True
		bast_line = BlastAlignment(debug, use_multithreading)
		previous_begin = 13
		bast_line.add_query(previous_begin, seq_a, len(seq_a) + previous_begin)
		bast_line.add_subject(13, seq_b, 20)
		
		bast_line.make_cigar_string()
		self.assertEqual("AAAAAACA---TACAAAAT", bast_line.get_query_sequence())
		self.assertEqual("AAAAAACAAAATA-A---T", bast_line.get_subject_sequence())
		self.assertEqual(7, len(bast_line.synchronize.vect_data))
		self.assertTrue(SyncHoles(8, SyncHoles.QUERY) == bast_line.synchronize.vect_data[0])
		self.assertTrue(SyncHoles(9, SyncHoles.QUERY) == bast_line.synchronize.vect_data[1])
		self.assertTrue(SyncHoles(10, SyncHoles.QUERY) == bast_line.synchronize.vect_data[2])
		self.assertTrue(SyncHoles(13, SyncHoles.SUBJECT) == bast_line.synchronize.vect_data[3])
		self.assertTrue(SyncHoles(15, SyncHoles.SUBJECT) == bast_line.synchronize.vect_data[4])
		self.assertTrue(SyncHoles(16, SyncHoles.SUBJECT) == bast_line.synchronize.vect_data[5])
		self.assertTrue(SyncHoles(17, SyncHoles.SUBJECT) == bast_line.synchronize.vect_data[6])
		self.assertEqual(cigar, bast_line.get_cigar().get_vect_cigar_string())

		#### new test
		seq_a = "AAAAAAC---ATACAAAAAT"
		seq_b = "AAAAAACAAAATA----AAT"
		cigar = ["8M3I2M1D2M3D1M"]
		
		use_multithreading = False
		debug = True
		bast_line = BlastAlignment(debug, use_multithreading)
		previous_begin = 13
		bast_line.add_query(previous_begin, seq_a, len(seq_a) + previous_begin)
		bast_line.add_subject(13, seq_b, 20)
		
		bast_line.make_cigar_string()
		self.assertEqual("AAAAAACA---TACAAAAAT", bast_line.get_query_sequence())
		self.assertEqual("AAAAAACAAAATA-AA---T", bast_line.get_subject_sequence())
		self.assertEqual(cigar, bast_line.get_cigar().get_vect_cigar_string())


		#### new test
		seq_a = "AAAAAAC---ATAC----AAT"
		seq_b = "AAAAAACAAAATACAAAAAAT"
		cigar = ["8M3I5M4I1M"]
		
		use_multithreading = False
		debug = True
		bast_line = BlastAlignment(debug, use_multithreading)
		previous_begin = 13
		bast_line.add_query(previous_begin, seq_a, len(seq_a) + previous_begin)
		bast_line.add_subject(13, seq_b, 20)
		
		bast_line.make_cigar_string()
		self.assertEqual("AAAAAACA---TACAA----T", bast_line.get_query_sequence())
		self.assertEqual("AAAAAACAAAATACAAAAAAT", bast_line.get_subject_sequence())
		self.assertEqual(cigar, bast_line.get_cigar().get_vect_cigar_string())

		#### new test
		seq_a = "AAAAAAC---ATAC----AAT"
		seq_b = "AAAAAACAAAATACAAAAAAT"
		cigar = ["8M3I5M4I1M"]
		
		use_multithreading = False
		debug = True
		bast_line = BlastAlignment(debug, use_multithreading)
		previous_begin = 13
		bast_line.add_query(previous_begin, seq_a, len(seq_a) + previous_begin)
		bast_line.add_subject(13, seq_b, 20)
		
		bast_line.make_cigar_string()
		self.assertEqual("AAAAAACA---TACAA----T", bast_line.get_query_sequence())
		self.assertEqual("AAAAAACAAAATACAAAAAAT", bast_line.get_subject_sequence())
		self.assertEqual(cigar, bast_line.get_cigar().get_vect_cigar_string())

		#### new test
		seq_a = "GGCCAAGAAGAAGGAAGAAGAGGCCAAG"
		seq_b = "GGCC---AAGAAGGCAGAGGAAGCCAAG"
		cigar = ["10M2D1M1D14M"]
		
		use_multithreading = False
		debug = True
		bast_line = BlastAlignment(debug, use_multithreading)
		previous_begin = 13
		bast_line.add_query(previous_begin, seq_a, len(seq_a) + previous_begin)
		bast_line.add_subject(13, seq_b, 20)
		
		bast_line.make_cigar_string()
		self.assertEqual("GGCCAAGAAGAAGGAAGAAGAGGCCAAG", bast_line.get_query_sequence())
		self.assertEqual("GGCCAAGAAG--G-CAGAGGAAGCCAAG", bast_line.get_subject_sequence())
		self.assertEqual(cigar, bast_line.get_cigar().get_vect_cigar_string())



	def test_dash(self):
		
		blast_descritpion = BlastDescritpion()
		blast_descritpion.add_sequence("AAAAAAAAAAAAAAAAAAAAAAA")
		self.assertFalse(blast_descritpion.has_dash())
		blast_descritpion = BlastDescritpion()
		blast_descritpion.add_sequence("AAAAAAAAAAAAAAAAAAAAAA-")
		self.assertTrue(blast_descritpion.has_dash())
		blast_descritpion = BlastDescritpion()
		blast_descritpion.add_sequence("AA-AAAAAAAAAAAAAAAAAAA-")
		self.assertTrue(blast_descritpion.has_dash())
		self.assertEqual([2, 22], blast_descritpion.vect_holes)
		blast_descritpion = BlastDescritpion()
		blast_descritpion.add_sequence("AA-AAAAAAAAAAAAAAAAAAA--CAAAAAAAAAAAAAAAAAAAA-")
		self.assertEqual([2, 22, 23, 45], blast_descritpion.get_holes())
		
		self.assertEqual(('A', 3), blast_descritpion.get_next_base(2))
		self.assertEqual(('C', 24), blast_descritpion.get_next_base(22))
		self.assertEqual(('', -1), blast_descritpion.get_next_base(45))
		
		blast_descritpion.set_base('G', 23)
		self.assertEqual(('G', 23), blast_descritpion.get_next_base(22))

	def test_parse_blast_2(self):
		
		utils = Utils()
		print("Processing chromosome: Ca22chr6X_C_albicans_SC5314")
		use_multithreading = False
		seq_file_name_a = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/ref/Ca22chr6A_C_albicans_SC5314.fasta.gz")
		seq_file_name_b = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/ref/Ca22chr6B_C_albicans_SC5314.fasta.gz")
		self.assertTrue(os.path.exists(seq_file_name_a))
		self.assertTrue(os.path.exists(seq_file_name_b))
		
		temp_1 = utils.get_temp_file("to_test_", ".fasta")
		temp_2 = utils.get_temp_file("to_test_", ".fasta")
		
		### unzio files
		utils.unzip(seq_file_name_a, temp_1)
		utils.unzip(seq_file_name_b, temp_2)
		
		debug = True
		blast_two_sequences = BlastTwoSequences(temp_1, temp_2, debug, use_multithreading)
		blast_alignments = blast_two_sequences.align_data()
		
		ref_1 = Reference(seq_file_name_a)
		ref_2 = Reference(seq_file_name_b)
		count_elements = blast_alignments.get_cigar_count_elements()
		self.assertEqual("1033112\t1033032\t0", str(count_elements))
		self.assertEqual("99.98", "{:.2f}".format(count_elements.get_percentage_coverage(\
							ref_1.get_chr_length('Ca22chr6A_C_albicans_SC5314'),\
							ref_2.get_chr_length('Ca22chr6B_C_albicans_SC5314'))) )
		utils.remove_file(temp_1)
		utils.remove_file(temp_2)


	def test_parse_blast_3(self):
		
		utils = Utils()
		print("Processing chromosome: Ca22chr2X_C_albicans_SC5314")
		use_multithreading = False
		seq_file_name_a = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/ref/Ca22chr2A_C_albicans_SC5314.fasta.gz")
		seq_file_name_b = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/ref/Ca22chr2B_C_albicans_SC5314.fasta.gz")
		self.assertTrue(os.path.exists(seq_file_name_a))
		self.assertTrue(os.path.exists(seq_file_name_b))
		
		temp_1 = utils.get_temp_file("to_test_", ".fasta")
		temp_2 = utils.get_temp_file("to_test_", ".fasta")
		
		### unzio files
		utils.unzip(seq_file_name_a, temp_1)
		utils.unzip(seq_file_name_b, temp_2)
		
		debug = True
		blast_two_sequences = BlastTwoSequences(temp_1, temp_2, debug, use_multithreading)
		blast_alignments = blast_two_sequences.align_data()
		blast_alignments.print_all_alignments()
		
		ref_1 = Reference(seq_file_name_a)
		ref_2 = Reference(seq_file_name_b)
		count_elements = blast_alignments.get_cigar_count_elements()
		self.assertEqual("2229805\t2229721\t0", str(count_elements))
		self.assertEqual("99.91", "{:.2f}".format(count_elements.get_percentage_coverage(\
							ref_1.get_chr_length('Ca22chr2A_C_albicans_SC5314'),\
							ref_2.get_chr_length('Ca22chr2B_C_albicans_SC5314'))) )
		utils.remove_file(temp_1)
		utils.remove_file(temp_2)



# Query  10997  AAAGAAGAAGCGGCAAGAAAGAAACGTGAAGAAGAGGCCAAGAAGAAGGAAGAAGAGGCC  11056
#               || ||||||| ||| | |||| || | | ||| |||||||||||||||||||||||||||
# Sbjct  11042  AAGGAAGAAGAGGCCAAAAAG-AA-G-GCAGAGGAGGCCAAGAAGAAGGAAGAAGAGGCC  11098
# 
# Query  11057  AAAAAGAAGGCAGAGGAGGCCAAGAAGAAGGAAGAAGAGGCCAAGAAAGCAGA-GGAG--  11113
#                  ||||| ||||||||||||   ||||||| ||| || |||||||| | ||| | ||  
# Sbjct  11099  ---AAGAAAGCAGAGGAGGCC---AAGAAGGCAGAGGAAGCCAAGAAGGTAGAAGAAGCA  11152
# 
# Query  11114  GCCAAGAAGGCAGAGGAAGCCAAGAAGGTAGAAGAAGCAGCCA-A--GAAGGCAGAG  11167
#               |||||||||||||||||||||||||| | ||||||||  |||| |  ||| ||||||
# Sbjct  11153  GCCAAGAAGGCAGAGGAAGCCAAGAAAGCAGAAGAAGAGGCCAGAAAGAAAGCAGAG  11209

if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.test_parse_blast']
	unittest.main()