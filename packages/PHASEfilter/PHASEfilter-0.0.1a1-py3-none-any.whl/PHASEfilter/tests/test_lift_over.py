'''
Created on 10/12/2019

@author: mmp
'''
import unittest, os
from PHASEfilter.lib.utils.util import Utils
from PHASEfilter.lib.utils.reference import Reference
from PHASEfilter.lib.utils.lift_over_simple import LiftOverLight
from PHASEfilter.lib.utils.lift_over_simple import Cigar
from PHASEfilter.lib.utils.software import Software

class Test(unittest.TestCase):

	
	def test_gicar_strings(self):
		cigar_string = "53S487M60I26M1D69M3I90M1D130M3I318M"

		cigar = Cigar([cigar_string])
		self.assertEqual((-1, -1), cigar.get_position_from_2_to(-1))
		self.assertEqual((-1, -1), cigar.get_position_from_2_to(0))
		self.assertEqual((54, -1), cigar.get_position_from_2_to(1))
		self.assertEqual((106, -1), cigar.get_position_from_2_to(53))
		self.assertEqual((107, -1), cigar.get_position_from_2_to(54))
		self.assertEqual((540, -1), cigar.get_position_from_2_to(487))
		self.assertEqual((714, -1), cigar.get_position_from_2_to(599))
		self.assertEqual((715, -1), cigar.get_position_from_2_to(600))
		self.assertEqual((716, -1), cigar.get_position_from_2_to(601))
		self.assertEqual((-1, -1), cigar.get_position_from_2_to(11601))

		self.assertEqual("length query\tlength subject\tmissmatch", str(cigar.count_length.get_header()))
		self.assertEqual("1122\t1186\t53", str(cigar.count_length))
		self.assertEqual(1122, cigar.count_length.get_lenth_query())
		self.assertEqual(1186, cigar.count_length.get_lenth_subject())
		self.assertEqual("51.3", "{:.1f}".format(cigar.count_length.get_percentage_coverage(2000, 2500)))
		self.assertEqual("100.0", "{:.1f}".format(cigar.count_length.get_percentage_coverage(1122, 1186)))
		self.assertEqual("97.8", "{:.1f}".format(cigar.count_length.get_percentage_coverage(1122, 1186 + 53)))


	def test_gicar_strings_2(self):
		cigar_string = "35769M1I9181M1I1214M1I77659M1D2788M1D4135M1D3274M1D69M3I90M1D130M"+\
		"3I645M1D343M1D1499M2D175M1I236M3I318M2I536M1I139M1D124M1D129M1I26M2D2566M3D688M1"+\
		"I102M3D513M3D170M2I150M3D93M1D39M2I31M1D151M1I712M1I268M1I268M3I324M1D1003M2I146"+\
		"M3I172M3I8M1D159M3I103M1D2440M1D1053M1D810M1D1558M2D111M3D932M2I837M2I457M1D234M"+\
		"1I783M1D3086M1D3874M3D2170M1I633M2I785M1D68M1I288M1I2117M3I3979M1I1350M1I48M2I27"+\
		"8M2D4527M1I11651M1D533M1D12877M1I1469M1D1280M2I2440M2I153M1D26934M1I2551M1D6648M"+\
		"1I9870M1D18M1I6870M1I6358M1I1870M1I9926M1D4330M2I162M1D7082M1D4M1D1140M2I236M1I1"+\
		"921M1I2372M1I4623M1I105M3I730M1D715M1I2600M1D2508M1D4439M1I5492M1D232M1D34M1I780"+\
		"M1I5270M1I1261M1D1489M1I724M1I103M1D2742M1I1407M2D37M1I189M1I54M1D352M1I2869M1D3"+\
		"70M1D5387M1D2226M1D51M3I48M1I476M1D181M1D52M3D1423M3D2722M2I85M1D218M1I1441M3I29"+\
		"50M1D397M2I898M2I31M1D616M3D723M1D286M1D237M1I14958M1I16M1I117M2D311M1D7434M1D16"+\
		"0M2D36M1D1392M1D1303M1D6282M1D84M1I41M2D6004M1D5422M2I11930M2I177M1I264M3I3502M1"+\
		"I4296M2I255M1I5722M1I396M1D381M1D1852M1D2890M2D6004M1D96M1I518M1I13095M2D10126M3"+\
		"I3056M3D42M3D2745M2I248M2I145M1D169M1I131M1D4655M1D26M3I37M1I206M2I177M2I473M2D3"+\
		"5M3I538M1D75M2I2402M1D51M2D4656M1I2668M1D68M1D1898M1D63M1D546M2D681M1I195M2I334M"+\
		"1I6661M3I1530M1I2556M1I2825M1I33M1D58M2I831M3I629M3I159M1D146M2D41M1D25M1D1669M1"+\
		"D214M3I38M2D96M1D14M1I66M1I5888M1I273M1D932M2D265M1I37M1D60M1I994M2D989M1D119M1I"+\
		"61M1I212M6I1810M1I447M3D1209M2I113M2D3871M2I11166M1I24M1I262M1D298M3I553M1I405M1"+\
		"D7649M1D192M1I24M1D178M2D16M1I906M1I15M1D4472M1D4261M1D43M1D707M2D4196M3I3111M2I"+\
		"9212M3D29M2I716M1D17068M2D4759M1I38M1D2263M1D843M1I77M1I880M1D44M1D2674M2I6365M2"+\
		"I1068M1I2290M1D76M1I4412M1I20M1D3242M1D497M1D1527M1I240M1D1853M2D224M1D1433M1I69"+\
		"1M2I203M1D1445M1D1591M1I94M1D2329M1D4650M1I280M1I100M1I6676M1I2636M1D357M1I343M1"+\
		"I4865M1I13636M1I331M2I123M1D2572M1I244M1I839M1I4532M2I21858M1D2995M2I98M1D8905M1"+\
		"I3205M1D9858M1D250M1I218M1I7480M1I3315M1I2258M1D3923M1D3594M1I1992M1D2527M1D1958"+\
		"M1D1444M1I3935M3I641M2I5266M1I1909M1D277M1D1787M3I3114M2I1675M1I4450M3I217M1D106"+\
		"8M2D1575M1D2161M1D4424M3D152M1D180M1D3473M1I724M2I5252M1D3398M1I354M1D69M1I19M1D"+\
		"687M1I574M1I1482M1D165M2I2481M3I641M1I26M1D1218M1I3963M1D631M1I388M1D5054M2I249M"+\
		"2I75M2I375M1I1029M1I2936M3D486M1I1282M2I843M1I473M1D139M3D413M1I318M1I147M3I515M"

		cigar = Cigar([cigar_string])
		self.assertEqual((759739, -1), cigar.get_position_from_2_to(759690))
		self.assertEqual((-1, 759825), cigar.get_position_from_2_to(759777))

	def test_gicar_strings_3(self):

		utils = Utils()
		seq_file_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/synchronize/chrB.txt")
		self.assertTrue(os.path.exists(seq_file_name))
		vect_result = utils.read_text_file(seq_file_name)
		self.assertEqual(2, len(vect_result))
		
		cigar = Cigar(vect_result)
		self.assertEqual((-1, -1), cigar.get_position_from_2_to(1559505))
		self.assertEqual((-1, -1), cigar.get_position_from_2_to(557668))


	def test_list_over_simple(self):
		
		utils = Utils("synchronize")
		temp_work_dir = utils.get_temp_dir()
		
		seq_file_name_a = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/ref/first_file_a.fasta")
		seq_file_name_b = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/ref/first_file_b.fasta")
		self.assertTrue(os.path.exists(seq_file_name_a))
		self.assertTrue(os.path.exists(seq_file_name_b))
		
		reference_a = Reference(seq_file_name_a)
		reference_b = Reference(seq_file_name_b)
		impose_minimap2_only = False
		lift_over_ligth = LiftOverLight(reference_a, reference_b, temp_work_dir, impose_minimap2_only)
		
		seq_name_a = reference_a.get_first_seq()
		self.assertEqual("A", seq_name_a)
		seq_name_b = reference_b.get_chr_in_genome(seq_name_a)
		self.assertEqual("A", seq_name_b)
		lift_over_ligth.synchronize_sequences(seq_name_a, seq_name_b)
		
		## S -> soft clipping (clipped sequences present in SEQ)
		## H -> hard clipping (clipped sequences NOT present in SEQ)
		## minimap2
		self.assertEqual(["53S487M60I26M1D69M3I90M1D130M3I318M"], lift_over_ligth.get_cigar_string(\
			Software.SOFTWARE_minimap2_name, seq_name_a, seq_name_b))
		self.assertEqual((54, -1), lift_over_ligth.get_pos_in_target(seq_name_a, seq_name_b, 1))
		self.assertEqual((60, -1), lift_over_ligth.get_pos_in_target(seq_name_a, seq_name_b, 7))
		self.assertEqual((540, -1), lift_over_ligth.get_pos_in_target(seq_name_a, seq_name_b, 487))
		self.assertEqual((480, -1), lift_over_ligth.get_pos_in_target(seq_name_a, seq_name_b, 427))
		self.assertEqual((779, -1), lift_over_ligth.get_pos_in_target(seq_name_a, seq_name_b, 664))
		self.assertEqual("1122\t1186\t53", str(lift_over_ligth.get_count_cigar_length(\
			Software.SOFTWARE_minimap2_name, seq_name_a, seq_name_b)))
		self.assertEqual("94.55", "{:.2f}".format(lift_over_ligth.get_percent_alignment(Software.SOFTWARE_minimap2_name, seq_name_a, seq_name_b)))
		
		## lastz
		self.assertEqual(["487M60I26M1D70M3I89M1D130M3I318M"], lift_over_ligth.get_cigar_string(\
			Software.SOFTWARE_lastz_name, seq_name_a, seq_name_b))
		self.assertEqual("1122\t1186\t0", str(lift_over_ligth.get_count_cigar_length(\
			Software.SOFTWARE_lastz_name, seq_name_a, seq_name_b)))
		self.assertEqual((54, -1), lift_over_ligth.get_pos_in_target(seq_name_a, seq_name_b, 1, Software.SOFTWARE_lastz_name))
		self.assertEqual((60, -1), lift_over_ligth.get_pos_in_target(seq_name_a, seq_name_b, 7, Software.SOFTWARE_lastz_name))
		self.assertEqual((540, -1), lift_over_ligth.get_pos_in_target(seq_name_a, seq_name_b, 487, Software.SOFTWARE_lastz_name))
		self.assertEqual((480, -1), lift_over_ligth.get_pos_in_target(seq_name_a, seq_name_b, 427, Software.SOFTWARE_lastz_name))
		self.assertEqual((779, -1), lift_over_ligth.get_pos_in_target(seq_name_a, seq_name_b, 664, Software.SOFTWARE_lastz_name))
		self.assertEqual("94.55", "{:.2f}".format(lift_over_ligth.get_percent_alignment(Software.SOFTWARE_lastz_name, seq_name_a, seq_name_b)))
		
		## blast
		self.assertEqual(['488M', '42M1D59M3I100M1D137M2I1M1I300M'], lift_over_ligth.get_cigar_string(\
			Software.SOFTWARE_blast_name, seq_name_a, seq_name_b))
		self.assertEqual("1122\t1133\t0", str(lift_over_ligth.get_count_cigar_length(\
			Software.SOFTWARE_blast_name, seq_name_a, seq_name_b)))
		self.assertEqual((54, -1), lift_over_ligth.get_pos_in_target(seq_name_a, seq_name_b, 1, Software.SOFTWARE_blast_name))
		self.assertEqual((60, -1), lift_over_ligth.get_pos_in_target(seq_name_a, seq_name_b, 7, Software.SOFTWARE_blast_name))
		self.assertEqual((540, -1), lift_over_ligth.get_pos_in_target(seq_name_a, seq_name_b, 487, Software.SOFTWARE_blast_name))
		self.assertEqual((480, -1), lift_over_ligth.get_pos_in_target(seq_name_a, seq_name_b, 427, Software.SOFTWARE_blast_name))
		self.assertEqual((779, -1), lift_over_ligth.get_pos_in_target(seq_name_a, seq_name_b, 664, Software.SOFTWARE_blast_name))
		self.assertEqual("92.38", "{:.2f}".format(lift_over_ligth.get_percent_alignment(Software.SOFTWARE_blast_name, seq_name_a, seq_name_b)))
		
		
		#### save alignment file
		temp_out_file = utils.get_temp_file_with_path(temp_work_dir, "align", ".aln")
		method = Software.SOFTWARE_minimap2_name
		temp_out_file = lift_over_ligth.create_alignment_file(temp_out_file, method, seq_name_a, seq_name_b)
		self.assertFalse(temp_out_file is None)
		self.assertTrue(os.path.exists(temp_out_file))
		
		### comp files
		out_result_expected = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/ref/expect_file_align_clustalx.fasta")
		self.assertTrue(os.path.exists(out_result_expected))
		temp_diff = utils.get_temp_file_with_path(temp_work_dir, "diff_file", ".txt")
		print(temp_out_file)
		print(out_result_expected)
		cmd = "diff {} {} > {}".format(temp_out_file, out_result_expected, temp_diff)
		os.system(cmd)
		vect_result = utils.read_text_file(temp_diff)
		print("{}".join("\n".join(vect_result)))
		self.assertEqual(0, len(vect_result))
		
		utils.remove_dir(temp_work_dir)
		utils.remove_dir(temp_diff)


	def test_list_over_simple_2(self):
		utils = Utils("synchronize")
		temp_work_dir = utils.get_temp_dir()
		
		seq_file_name_a = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/ref/second_file_a.fasta")
		seq_file_name_b = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/ref/second_file_b.fasta")
		self.assertTrue(os.path.exists(seq_file_name_a))
		self.assertTrue(os.path.exists(seq_file_name_b))
		
		reference_a = Reference(seq_file_name_a)
		reference_b = Reference(seq_file_name_b)
		impose_minimap2_only = True
		lift_over_ligth = LiftOverLight(reference_a, reference_b, temp_work_dir, impose_minimap2_only, True)
		
		seq_name_a = reference_a.get_first_seq()
		self.assertEqual("A", seq_name_a)
		seq_name_b = reference_b.get_chr_in_genome(seq_name_a)
		self.assertEqual("B", seq_name_b)
		lift_over_ligth.synchronize_sequences(seq_name_a, seq_name_b)
		
		self.assertEqual(['96S92M'], lift_over_ligth.get_cigar_string(\
			Software.SOFTWARE_minimap2_name, seq_name_a, seq_name_b))
		self.assertEqual((144, -1), lift_over_ligth.get_pos_in_target(seq_name_a, seq_name_b, 48))
		self.assertEqual((145, -1), lift_over_ligth.get_pos_in_target(seq_name_a, seq_name_b, 49))
		self.assertEqual((-1, -1), lift_over_ligth.get_pos_in_target(seq_name_a, seq_name_b, 490))
		self.assertEqual("92\t92\t96", str(lift_over_ligth.get_count_cigar_length(\
			Software.SOFTWARE_minimap2_name, seq_name_a, seq_name_b)))
		self.assertEqual(1, lift_over_ligth.get_number_cigar_string(\
			Software.SOFTWARE_minimap2_name, seq_name_a, seq_name_b))
		utils.remove_dir(temp_work_dir)
		
	def test_list_over_simple_3(self):
		utils = Utils("synchronize")
		temp_work_dir = utils.get_temp_dir()
		
		seq_file_name_a = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/ref/second_file_b.fasta")
		seq_file_name_b = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/ref/second_file_a.fasta")
		self.assertTrue(os.path.exists(seq_file_name_a))
		self.assertTrue(os.path.exists(seq_file_name_b))
		
		reference_a = Reference(seq_file_name_a)
		reference_b = Reference(seq_file_name_b)
		impose_minimap2_only = True
		lift_over_ligth = LiftOverLight(reference_a, reference_b, temp_work_dir, impose_minimap2_only, True)
		
		seq_name_a = reference_a.get_first_seq()
		self.assertEqual("B", seq_name_a)
		seq_name_b = reference_b.get_chr_in_genome(seq_name_a)
		self.assertEqual("A", seq_name_b)
		lift_over_ligth.synchronize_sequences(seq_name_a, seq_name_b)
		
		self.assertEqual(["92M"], lift_over_ligth.get_cigar_string(\
			Software.SOFTWARE_minimap2_name, seq_name_a, seq_name_b))
		self.assertEqual((48, -1), lift_over_ligth.get_pos_in_target(seq_name_a, seq_name_b, 48))
		self.assertEqual((53, -1), lift_over_ligth.get_pos_in_target(seq_name_a, seq_name_b, 53))
		self.assertEqual((54, -1), lift_over_ligth.get_pos_in_target(seq_name_a, seq_name_b, 54))
		self.assertEqual((49, -1), lift_over_ligth.get_pos_in_target(seq_name_a, seq_name_b, 49))
		self.assertEqual((52, -1), lift_over_ligth.get_pos_in_target(seq_name_a, seq_name_b, 52))
		self.assertEqual((-1, -1), lift_over_ligth.get_pos_in_target(seq_name_a, seq_name_b, 100))
		self.assertEqual((-1, -1), lift_over_ligth.get_pos_in_target(seq_name_a, seq_name_b, 490))
		utils.remove_dir(temp_work_dir)


# 	def test_list_over_saccharo_chr_xi(self):
# 		utils = Utils("synchronize")
# 		temp_work_dir = utils.get_temp_dir()
# 		
# 		seq_file_name_a = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/referenceSaccharo/chrX.fasta")
# 		seq_file_name_b = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/referenceSaccharo/S01.chrX.fasta")
# 		self.assertTrue(os.path.exists(seq_file_name_a))
# 		self.assertTrue(os.path.exists(seq_file_name_b))
# 		
# 		reference_a = Reference(seq_file_name_a)
# 		reference_b = Reference(seq_file_name_b)
# 		impose_minimap2_only = False
# 		lift_over_ligth = LiftOverLight(reference_a, reference_b, temp_work_dir, impose_minimap2_only, True)
# 		lift_over_ligth.synchronize_sequences("chrX", "chrX")
# 
# 		self.assertEqual((-1, -1), lift_over_ligth.get_best_pos_in_target("chrX", "chrX", 48))
# 		self.assertEqual((29, -1), lift_over_ligth.get_best_pos_in_target("chrX", "chrX", 168))
# 		self.assertEqual((177, -1), lift_over_ligth.get_best_pos_in_target("chrX", "chrX", 300))
# 		utils.remove_dir(temp_work_dir)
# 	
# 	def test_list_over_saccharo_chr_xi_small(self):
# 		utils = Utils("synchronize")
# 		temp_work_dir = utils.get_temp_dir()
# 		
# 		seq_file_name_a = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/referenceSaccharo/chrX_small.fasta")
# 		seq_file_name_b = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/referenceSaccharo/S01_chrX_small.fasta")
# 		self.assertTrue(os.path.exists(seq_file_name_a))
# 		self.assertTrue(os.path.exists(seq_file_name_b))
# 		
# 		reference_a = Reference(seq_file_name_a)
# 		reference_b = Reference(seq_file_name_b)
# 		impose_minimap2_only = False
# 		lift_over_ligth = LiftOverLight(reference_a, reference_b, temp_work_dir, impose_minimap2_only, True)
# 		lift_over_ligth.synchronize_sequences("chrX", "chrX")
# 
# 		self.assertEqual((246, -1), lift_over_ligth.get_best_pos_in_target("chrX", "chrX", 48))
# 		self.assertEqual((438, -1), lift_over_ligth.get_best_pos_in_target("chrX", "chrX", 200))
# 		self.assertEqual((-1, 217), lift_over_ligth.get_best_pos_in_target("chrX", "chrX", 20))
# 		utils.remove_dir(temp_work_dir)


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.test_lift_over']
	unittest.main()
