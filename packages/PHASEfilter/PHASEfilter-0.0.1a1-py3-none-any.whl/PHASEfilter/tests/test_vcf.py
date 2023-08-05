'''
Created on 13/05/2020

@author: mmp
'''
import unittest, os
from PHASEfilter.lib.utils.util import Utils
from PHASEfilter.lib.utils.reference import Reference
from PHASEfilter.lib.utils.vcf_process import VcfProcess
from PHASEfilter.lib.utils.run_extra_software import RunExtraSoftware
from PHASEfilter.lib.utils.lift_over_simple import LiftOverLight
from PHASEfilter.lib.utils.software import Software

### run command line
# python3 -m unittest -v tests.test_vcf

class Test(unittest.TestCase):


	def setUp(self):
		pass


	def tearDown(self):
		pass


	def test_vcf(self):
	
		run_extra_software = RunExtraSoftware()
		utils = Utils("synchronize")
		temp_work_dir = utils.get_temp_dir()
		
		seq_file_name_a = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/ref/ref_ca22_1A.fasta")
		seq_file_name_b = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/ref/ref_ca22_1B.fasta")
		self.assertTrue(os.path.exists(seq_file_name_a))
		self.assertTrue(os.path.exists(seq_file_name_b))
		
		reference_a = Reference(seq_file_name_a)
		reference_b = Reference(seq_file_name_b)
		impose_minimap2_only = False
		lift_over_ligth = LiftOverLight(reference_a, reference_b, temp_work_dir, impose_minimap2_only, True)
		
		seq_name_a = reference_a.get_first_seq()
		self.assertEqual("Ca22chr1A_C_albicans_SC5314", seq_name_a)
		seq_name_b = reference_b.get_chr_in_genome(seq_name_a)
		self.assertEqual("Ca22chr1B_C_albicans_SC5314", seq_name_b)
		lift_over_ligth.synchronize_sequences(seq_name_a, seq_name_b)
		
		self.assertEqual(["35769M1I9181M1I1214M1I23763M"], lift_over_ligth.get_cigar_string(\
			Software.SOFTWARE_minimap2_name, seq_name_a, seq_name_b))
		self.assertEqual((487, -1), lift_over_ligth.get_pos_in_target(seq_name_a, seq_name_b, 487))
		
		#### read vcf
		vcf_file_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/vcf/chrA.vcf")
		self.assertTrue(os.path.exists(vcf_file_name))
		(temp_out_vcf_a, number_of_records) = run_extra_software.get_vcf_with_only_chr(vcf_file_name, seq_name_a, temp_work_dir)
		self.assertEqual(2209, number_of_records)
		
		vcf_file_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/vcf/chrB.vcf")
		self.assertTrue(os.path.exists(vcf_file_name))
		(temp_out_vcf_b, number_of_records) = run_extra_software.get_vcf_with_only_chr(vcf_file_name, seq_name_b, temp_work_dir)
		self.assertEqual(2209, number_of_records)
		
		vcf_out = utils.get_temp_file_with_path(temp_work_dir, "vcf_result", ".vcf")
		vcf_out_removed = utils.get_temp_file_with_path(temp_work_dir, "vcf_result_removed", ".vcf")
		b_print_results = False
		threshold_ad = 0.5
		vcf_process = VcfProcess(temp_out_vcf_a, threshold_ad, b_print_results)
		vcf_process.match_vcf_to(seq_name_a, lift_over_ligth, temp_out_vcf_b, seq_name_b, vcf_out, vcf_out_removed)
		self.assertTrue(vcf_process.count_alleles.has_removed_variants())
		self.assertTrue(vcf_process.count_alleles.has_saved_variants())
		
		self.assertEqual("Heterozygous (Removed)	Keep alleles	Other than SNP	Don't have hit position	Could Not Fetch VCF Record on Hit	Total alleles	Total Alleles new Source VCF", vcf_process.count_alleles.get_header())
		self.assertEqual("8	115	0	2078	8	2209	2201", str(vcf_process.count_alleles))
##		self.assertEqual("5	118	0	2078	8	2209	2204", str(vcf_process.count_alleles)) old line
		### test VCF
#####
# 0.5 Record(CHROM=Ca22chr1A_C_albicans_SC5314, POS=42297, REF=A, ALT=[T]) Record(CHROM=Ca22chr1B_C_albicans_SC5314, POS=42298, REF=T, ALT=[A])
# 0.5 Record(CHROM=Ca22chr1A_C_albicans_SC5314, POS=42343, REF=T, ALT=[C]) Record(CHROM=Ca22chr1B_C_albicans_SC5314, POS=42344, REF=C, ALT=[T])
# 0.5 Record(CHROM=Ca22chr1A_C_albicans_SC5314, POS=42635, REF=A, ALT=[G]) Record(CHROM=Ca22chr1B_C_albicans_SC5314, POS=42636, REF=G, ALT=[A])
# 0.5 Record(CHROM=Ca22chr1A_C_albicans_SC5314, POS=43315, REF=G, ALT=[T]) Record(CHROM=Ca22chr1B_C_albicans_SC5314, POS=43316, REF=T, ALT=[G])
# 0.5 Record(CHROM=Ca22chr1A_C_albicans_SC5314, POS=43334, REF=G, ALT=[A]) Record(CHROM=Ca22chr1B_C_albicans_SC5314, POS=43335, REF=A, ALT=[G])
# 0.5 Record(CHROM=Ca22chr1A_C_albicans_SC5314, POS=43353, REF=T, ALT=[C]) Record(CHROM=Ca22chr1B_C_albicans_SC5314, POS=43354, REF=C, ALT=[T])
# 0.5 Record(CHROM=Ca22chr1A_C_albicans_SC5314, POS=46307, REF=C, ALT=[G]) Record(CHROM=Ca22chr1B_C_albicans_SC5314, POS=46310, REF=G, ALT=[C])
# 0.5 Record(CHROM=Ca22chr1A_C_albicans_SC5314, POS=46450, REF=A, ALT=[G]) Record(CHROM=Ca22chr1B_C_albicans_SC5314, POS=46453, REF=G, ALT=[A])
# 		with open(vcf_out, 'r') as handle_in:
# 			vcf_reader = vcf.Reader(handle_in)
# 			for record in vcf_reader:
# 				print(record)


		### remove everything
		utils.remove_dir(temp_work_dir)
		utils.remove_file(temp_out_vcf_a)
		utils.remove_file(temp_out_vcf_a + ".tbi")
		utils.remove_file(temp_out_vcf_b)
		utils.remove_file(temp_out_vcf_b + ".tbi")


	def test_vcf_2(self):
	
		run_extra_software = RunExtraSoftware()
		utils = Utils("synchronize")
		temp_work_dir = utils.get_temp_dir()
		
		seq_file_name_a = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/ref/ref_ca22_1A.fasta")
		seq_file_name_b = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/ref/ref_ca22_1B.fasta")
		self.assertTrue(os.path.exists(seq_file_name_a))
		self.assertTrue(os.path.exists(seq_file_name_b))
		
		reference_a = Reference(seq_file_name_a)
		reference_b = Reference(seq_file_name_b)
		impose_minimap2_only = False
		lift_over_ligth = LiftOverLight(reference_a, reference_b, temp_work_dir, impose_minimap2_only, True)
		
		seq_name_a = reference_a.get_first_seq()
		self.assertEqual("Ca22chr1A_C_albicans_SC5314", seq_name_a)
		seq_name_b = reference_b.get_chr_in_genome(seq_name_a)
		self.assertEqual("Ca22chr1B_C_albicans_SC5314", seq_name_b)
		lift_over_ligth.synchronize_sequences(seq_name_a, seq_name_b)
		
		self.assertEqual(["35769M1I9181M1I1214M1I23763M"], lift_over_ligth.get_cigar_string(\
			Software.SOFTWARE_minimap2_name, seq_name_a, seq_name_b))
		self.assertEqual((487, -1), lift_over_ligth.get_pos_in_target(seq_name_a, seq_name_b, 487))
		
		#### read vcf
		vcf_file_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/vcf/chrA.vcf")
		self.assertTrue(os.path.exists(vcf_file_name))
		(temp_out_vcf_a, number_of_records) = run_extra_software.get_vcf_with_only_chr(vcf_file_name, seq_name_a, temp_work_dir)
		self.assertEqual(2209, number_of_records)
		
		vcf_file_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/vcf/chrB.vcf")
		self.assertTrue(os.path.exists(vcf_file_name))
		(temp_out_vcf_b, number_of_records) = run_extra_software.get_vcf_with_only_chr(vcf_file_name, seq_name_b, temp_work_dir)
		self.assertEqual(2209, number_of_records)
		
		vcf_out = utils.get_temp_file_with_path(temp_work_dir, "vcf_result", ".vcf")
		vcf_out_removed = utils.get_temp_file_with_path(temp_work_dir, "vcf_result_removed", ".vcf")
		b_print_results = False
		threshold_ad = 0.01
		vcf_process = VcfProcess(temp_out_vcf_a, threshold_ad, b_print_results)
		vcf_process.match_vcf_to(seq_name_a, lift_over_ligth, temp_out_vcf_b, seq_name_b, vcf_out, vcf_out_removed)
		self.assertTrue(vcf_process.count_alleles.has_removed_variants())
		self.assertTrue(vcf_process.count_alleles.has_saved_variants())
		
		self.assertEqual("Heterozygous (Removed)	Keep alleles	Other than SNP	Don't have hit position	Could Not Fetch VCF Record on Hit	Total alleles	Total Alleles new Source VCF", vcf_process.count_alleles.get_header())
		self.assertEqual("8	115	0	2078	8	2209	2201", str(vcf_process.count_alleles))
		### test VCF
#####
# 0.5 Record(CHROM=Ca22chr1A_C_albicans_SC5314, POS=42297, REF=A, ALT=[T]) Record(CHROM=Ca22chr1B_C_albicans_SC5314, POS=42298, REF=T, ALT=[A])
# 0.5 Record(CHROM=Ca22chr1A_C_albicans_SC5314, POS=42343, REF=T, ALT=[C]) Record(CHROM=Ca22chr1B_C_albicans_SC5314, POS=42344, REF=C, ALT=[T])
# 0.5 Record(CHROM=Ca22chr1A_C_albicans_SC5314, POS=42635, REF=A, ALT=[G]) Record(CHROM=Ca22chr1B_C_albicans_SC5314, POS=42636, REF=G, ALT=[A])
# 0.5 Record(CHROM=Ca22chr1A_C_albicans_SC5314, POS=43315, REF=G, ALT=[T]) Record(CHROM=Ca22chr1B_C_albicans_SC5314, POS=43316, REF=T, ALT=[G])
# 0.5 Record(CHROM=Ca22chr1A_C_albicans_SC5314, POS=43334, REF=G, ALT=[A]) Record(CHROM=Ca22chr1B_C_albicans_SC5314, POS=43335, REF=A, ALT=[G])
# 0.5 Record(CHROM=Ca22chr1A_C_albicans_SC5314, POS=43353, REF=T, ALT=[C]) Record(CHROM=Ca22chr1B_C_albicans_SC5314, POS=43354, REF=C, ALT=[T])
# 0.5 Record(CHROM=Ca22chr1A_C_albicans_SC5314, POS=46307, REF=C, ALT=[G]) Record(CHROM=Ca22chr1B_C_albicans_SC5314, POS=46310, REF=G, ALT=[C])
# 0.5 Record(CHROM=Ca22chr1A_C_albicans_SC5314, POS=46450, REF=A, ALT=[G]) Record(CHROM=Ca22chr1B_C_albicans_SC5314, POS=46453, REF=G, ALT=[A])
# 		with open(vcf_out, 'r') as handle_in:
# 			vcf_reader = vcf.Reader(handle_in)
# 			for record in vcf_reader:
# 				print(record)


		### remove everything
		utils.remove_dir(temp_work_dir)
		utils.remove_file(temp_out_vcf_a)
		utils.remove_file(temp_out_vcf_a + ".tbi")
		utils.remove_file(temp_out_vcf_b)
		utils.remove_file(temp_out_vcf_b + ".tbi")
		
	def test_vcf_indel(self):
		
		run_extra_software = RunExtraSoftware()
		utils = Utils("synchronize")
		temp_work_dir = utils.get_temp_dir()
		
		seq_file_name_a = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/ref/ref_ca22_1A.fasta")
		seq_file_name_b = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/ref/ref_ca22_1B.fasta")
		self.assertTrue(os.path.exists(seq_file_name_a))
		self.assertTrue(os.path.exists(seq_file_name_b))
		
		reference_a = Reference(seq_file_name_a)
		reference_b = Reference(seq_file_name_b)
		impose_minimap2_only = False
		lift_over_ligth = LiftOverLight(reference_a, reference_b, temp_work_dir, impose_minimap2_only, True)
		
		seq_name_a = reference_a.get_first_seq()
		self.assertEqual("Ca22chr1A_C_albicans_SC5314", seq_name_a)
		seq_name_b = reference_b.get_chr_in_genome(seq_name_a)
		self.assertEqual("Ca22chr1B_C_albicans_SC5314", seq_name_b)
		lift_over_ligth.synchronize_sequences(seq_name_a, seq_name_b)
		
		self.assertEqual(["35769M1I9181M1I1214M1I23763M"], lift_over_ligth.get_cigar_string(\
			Software.SOFTWARE_minimap2_name, seq_name_a, seq_name_b))
		self.assertEqual((487, -1), lift_over_ligth.get_pos_in_target(seq_name_a, seq_name_b, 487))
		
		#### read vcf
		vcf_file_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/vcf/A-M_S4_chrA_indel.vcf")
		self.assertTrue(os.path.exists(vcf_file_name))
		(temp_out_vcf_a, number_of_records) = run_extra_software.get_vcf_with_only_chr(vcf_file_name, seq_name_a, temp_work_dir)
		self.assertEqual(954, number_of_records)
		
		vcf_file_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/vcf/A-M_S4_chrB_indel.vcf")
		self.assertTrue(os.path.exists(vcf_file_name))
		(temp_out_vcf_b, number_of_records) = run_extra_software.get_vcf_with_only_chr(vcf_file_name, seq_name_b, temp_work_dir)
		self.assertEqual(954, number_of_records)
		
		vcf_out = utils.get_temp_file_with_path(temp_work_dir, "vcf_result", ".vcf")
		vcf_out_removed = utils.get_temp_file_with_path(temp_work_dir, "vcf_result_removed", ".vcf")
		b_print_results = False
		threshold_ad = 0.5
		vcf_process = VcfProcess(temp_out_vcf_a, threshold_ad, b_print_results)
		vcf_process.match_vcf_to(seq_name_a, lift_over_ligth, temp_out_vcf_b, seq_name_b, vcf_out, vcf_out_removed)
		self.assertTrue(vcf_process.count_alleles.has_removed_variants())
		self.assertTrue(vcf_process.count_alleles.has_saved_variants())
		
		self.assertEqual("Heterozygous (Removed)	Keep alleles	Other than SNP	Don't have hit position	Could Not Fetch VCF Record on Hit	Total alleles	Total Alleles new Source VCF", vcf_process.count_alleles.get_header())
		self.assertEqual("1	18	0	935	0	954	953", str(vcf_process.count_alleles))
		
		### remove everything
		utils.remove_dir(temp_work_dir)
		utils.remove_file(temp_out_vcf_a)
		utils.remove_file(temp_out_vcf_a + ".tbi")
		utils.remove_file(temp_out_vcf_b)
		utils.remove_file(temp_out_vcf_b + ".tbi")


	def test_vcf_ratio(self):
		
		b_print_results = False
		threshold_ad = 0.05
		vcf_process = VcfProcess(None, threshold_ad, b_print_results)
		self.assertEqual(0.1, vcf_process.get_ratio([200, 20], 1))
		self.assertEqual(0.1, vcf_process.get_ratio([20, 200], 1))
		self.assertEqual(0.5, vcf_process.get_ratio([20, 200], 2))
		self.assertEqual(0.0, vcf_process.get_ratio([0, 200], 1))
		self.assertEqual(1.0, vcf_process.get_ratio([0, 0], 1))
		self.assertEqual(0.0, vcf_process.get_ratio([10, 0], 1))
		self.assertEqual(0.01, vcf_process.get_ratio([20, 200, 2000], 2))

	def test_vcf_match_indels(self):
		
		b_print_results = False
		threshold_ad = 0.5
		vcf_process = VcfProcess(None, threshold_ad, b_print_results)
		
		slice_source = "GAAAAAAAAAAAGTGAAAATC"
		slice_hit = "GAAAAAAAAAAAAGTGAAAAT"
		ref_source = "G"
		alt_base_in_source = "GA"
		ref_hit = "GA"
		alt_base_in_hit = "G"
		(length_bases_after_base_source, length_bases_after_base_hit) = vcf_process.get_length_bases_match(slice_source,\
				slice_hit, ref_source, alt_base_in_source, ref_hit, alt_base_in_hit)
		self.assertEqual(12, length_bases_after_base_hit)
		self.assertEqual(11, length_bases_after_base_source)
		
		slice_source = "GAAAAAAAAAAAGTGAAAATC"
		slice_hit = "GAAAAAAAAAAAAGTGAAAAT"
		ref_source = "G"
		alt_base_in_source = "GAA"
		ref_hit = "GAA"
		alt_base_in_hit = "G"
		(length_bases_after_base_source, length_bases_after_base_hit) = vcf_process.get_length_bases_match(slice_source,\
				slice_hit, ref_source, alt_base_in_source, ref_hit, alt_base_in_hit)
		self.assertEqual(12, length_bases_after_base_hit)
		self.assertEqual(10, length_bases_after_base_source)

		slice_source = "GAAAAAAAAAAAAGTGAAAAT"
		slice_hit = "GAAAAAAAAAAAGTGAAAATC"
		ref_source = "G"
		alt_base_in_source = "GAA"
		ref_hit = "GAA"
		alt_base_in_hit = "G"
		(length_bases_after_base_source, length_bases_after_base_hit) = vcf_process.get_length_bases_match(slice_source,\
				slice_hit, ref_source, alt_base_in_source, ref_hit, alt_base_in_hit)
		self.assertEqual(10, length_bases_after_base_hit)
		self.assertEqual(12, length_bases_after_base_source)

		slice_source = "GAAAAAAAAAAAAGTGAAAAT"
		slice_hit = "GAAAAAAAGTGAAAATC"
		ref_source = "G"
		alt_base_in_source = "GAA"
		ref_hit = "GAA"
		alt_base_in_hit = "G"
		(length_bases_after_base_source, length_bases_after_base_hit) = vcf_process.get_length_bases_match(slice_source,\
				slice_hit, ref_source, alt_base_in_source, ref_hit, alt_base_in_hit)
		self.assertEqual(6, length_bases_after_base_hit)
		self.assertEqual(12, length_bases_after_base_source)
		
		slice_source = "GAAAAAAAAAAAA"
		slice_hit = "GAAAAAAAAAA"
		ref_source = "G"
		alt_base_in_source = "GAA"
		ref_hit = "GAA"
		alt_base_in_hit = "G"
		(length_bases_after_base_source, length_bases_after_base_hit) = vcf_process.get_length_bases_match(slice_source,\
				slice_hit, ref_source, alt_base_in_source, ref_hit, alt_base_in_hit)
		self.assertEqual(-1, length_bases_after_base_hit)
		self.assertEqual(-1, length_bases_after_base_source)
		
		slice_source = "AGAACTCAGAACTAAAAATAG"
		slice_hit = "AAACTCAGAACTAAAAATAGT"
		ref_source = "AG"
		alt_base_in_source = "A"
		ref_hit = "A"
		alt_base_in_hit = "AG"
		(length_bases_after_base_source, length_bases_after_base_hit) = vcf_process.get_length_bases_match(slice_source,\
				slice_hit, ref_source, alt_base_in_source, ref_hit, alt_base_in_hit)
		self.assertEqual(0, length_bases_after_base_hit)
		self.assertEqual(1, length_bases_after_base_source)


	def test_af_in_vcf(self):
		"""
		Test if vcf has AF tag
		"""
		
		vcf_file_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/vcf/test_with_AF_chrA.vcf")
		self.assertTrue(os.path.exists(vcf_file_name))
		b_print_results = False
		threshold_ad = 0.05
		vcf_process = VcfProcess(vcf_file_name, threshold_ad, b_print_results)
		self.assertFalse(vcf_process.has_format('AF'))
		self.assertTrue(vcf_process.has_format('AD'))
		
		vcf_file_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/vcf/test_without_AF_chrA.vcf")
		self.assertTrue(os.path.exists(vcf_file_name))
		b_print_results = False
		threshold_ad = 0.05
		vcf_process = VcfProcess(vcf_file_name, threshold_ad, b_print_results)
		self.assertFalse(vcf_process.has_format('AF'))
		self.assertTrue(vcf_process.has_format('DP'))
		self.assertFalse(vcf_process.has_format('MF'))

		
	def test_reference_file_name(self):
		"""
		test reference file name
		"""
		vcf_file_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/vcf/test_with_AF_chrA.vcf")
		self.assertTrue(os.path.exists(vcf_file_name))
		b_print_results = False
		threshold_ad = 0.05
		vcf_process = VcfProcess(vcf_file_name, threshold_ad, b_print_results)
		self.assertFalse(vcf_process.exist_reference_name('AF'))
		self.assertTrue(vcf_process.exist_reference_name('C_albicans_SC5314_A22_chromosomes.fasta'))


	def test_tag_test(self):
		"""
		test meta data tag
		"""
		vcf_file_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/vcf/test_with_AF_chrA.vcf")
		self.assertTrue(os.path.exists(vcf_file_name))
		b_print_results = False
		threshold_ad = 0.05
		vcf_process = VcfProcess(vcf_file_name, threshold_ad, b_print_results)
		self.assertFalse(vcf_process.exist_meta_data_tag('AF'))
		self.assertTrue(vcf_process.exist_meta_data_tag('reference'))
		self.assertTrue(vcf_process.exist_meta_data_tag('FORMAT'))


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()