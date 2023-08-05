

import unittest, os
from PHASEfilter.lib.utils.testing_software import SoftwareTest
from PHASEfilter.lib.utils.software import Software

class Test(unittest.TestCase):


	def setUp(self):
		pass


	def tearDown(self):
		pass

		
	def test_software_first(self):
		"""
		output: "name software
				1.5.rd2"
		"""
		
		software_test = SoftwareTest()
		SOFTWARE_test_1 = { 
				SoftwareTest.KEY_software_name : 'first', 
				SoftwareTest.KEY_software_run : os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files/software/first'), 
				SoftwareTest.KEY_software_run_get_version : os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files/software/first'), 
				SoftwareTest.KEY_version : '1.5',
				SoftwareTest.KEY_version_major_number : SoftwareTest.KEY_version_pass_equal,
				SoftwareTest.KEY_version_minor_number : SoftwareTest.KEY_version_pass_equal_or_bigger,
			}
		
		SOFTWARE_test_2 = { 
				SoftwareTest.KEY_software_name : 'first', 
				SoftwareTest.KEY_software_run : os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files/software/first'), 
				SoftwareTest.KEY_software_run_get_version : os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files/software/first'),
				SoftwareTest.KEY_version : '1.6',
				SoftwareTest.KEY_version_major_number : SoftwareTest.KEY_version_pass_equal,
				SoftwareTest.KEY_version_minor_number : SoftwareTest.KEY_version_pass_equal_or_bigger,
			}
		
		SOFTWARE_test_3 = { 
				SoftwareTest.KEY_software_name : 'first',
				SoftwareTest.KEY_software_run : os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files/software/first'), 
				SoftwareTest.KEY_software_run_get_version : os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files/software/first'),
				SoftwareTest.KEY_version : '2.3',
				SoftwareTest.KEY_version_major_number : SoftwareTest.KEY_version_pass_equal,
				SoftwareTest.KEY_version_minor_number : SoftwareTest.KEY_version_pass_equal_or_bigger,
			}
		
		SOFTWARE_test_4 = { 
				SoftwareTest.KEY_software_name : 'first',
				SoftwareTest.KEY_software_run : os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files/software/first'), 
				SoftwareTest.KEY_software_run_get_version : os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files/software/first'),
				SoftwareTest.KEY_version : '1.4',
				SoftwareTest.KEY_version_major_number : SoftwareTest.KEY_version_pass_equal,
				SoftwareTest.KEY_version_minor_number : SoftwareTest.KEY_version_pass_equal_or_bigger,
			}
		
		
		self.assertTrue(software_test.test_software(SOFTWARE_test_1))
		self.assertFalse(software_test.test_software(SOFTWARE_test_2))
		self.assertFalse(software_test.test_software(SOFTWARE_test_3))
		self.assertTrue(software_test.test_software(SOFTWARE_test_4))
	
	
	def test_software_second(self):
		"""
		output: "version: 1.5.43"
		"""
		
		software_test = SoftwareTest()
		SOFTWARE_test_1 = { 
				SoftwareTest.KEY_software_name : 'second',
				SoftwareTest.KEY_software_run : os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files/software/second'), 
				SoftwareTest.KEY_software_run_get_version : os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files/software/second'),
				SoftwareTest.KEY_version : '1.5',
				SoftwareTest.KEY_version_major_number : SoftwareTest.KEY_version_pass_equal,
				SoftwareTest.KEY_version_minor_number : SoftwareTest.KEY_version_pass_equal_or_bigger,
			}
		
		SOFTWARE_test_2 = { 
				SoftwareTest.KEY_software_name : 'second',
				SoftwareTest.KEY_software_run : os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files/software/second'),
				SoftwareTest.KEY_software_run_get_version : os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files/software/second'),
				SoftwareTest.KEY_version : '1.6',
				SoftwareTest.KEY_version_major_number : SoftwareTest.KEY_version_pass_equal,
				SoftwareTest.KEY_version_minor_number : SoftwareTest.KEY_version_pass_equal_or_bigger,
			}
		
		SOFTWARE_test_3 = { 
				SoftwareTest.KEY_software_name : 'second',
				SoftwareTest.KEY_software_run : os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files/software/second'), 
				SoftwareTest.KEY_software_run_get_version : os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files/software/second'),
				SoftwareTest.KEY_version : '2.3',
				SoftwareTest.KEY_version_major_number : SoftwareTest.KEY_version_pass_equal,
				SoftwareTest.KEY_version_minor_number : SoftwareTest.KEY_version_pass_equal_or_bigger,
			}
		
		SOFTWARE_test_4 = { 
				SoftwareTest.KEY_software_name : 'second',
				SoftwareTest.KEY_software_run : os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files/software/second'),
				SoftwareTest.KEY_software_run_get_version : os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files/software/second'),
				SoftwareTest.KEY_version : '1.4',
				SoftwareTest.KEY_version_major_number : SoftwareTest.KEY_version_pass_equal,
				SoftwareTest.KEY_version_minor_number : SoftwareTest.KEY_version_pass_equal_or_bigger,
			}
		
		SOFTWARE_test_5 = { 
				SoftwareTest.KEY_software_name : 'second',
				SoftwareTest.KEY_software_run : os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files/software/second'),
				SoftwareTest.KEY_software_run_get_version : os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files/software/second'),
				SoftwareTest.KEY_version : '2.3',
				SoftwareTest.KEY_version_major_number : SoftwareTest.KEY_version_pass_equal_or_bigger,
				SoftwareTest.KEY_version_minor_number : SoftwareTest.KEY_version_pass_equal_or_bigger,
			}
		SOFTWARE_test_6 = { 
				SoftwareTest.KEY_software_name : 'second',
				SoftwareTest.KEY_software_run : os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files/software/second'),
				SoftwareTest.KEY_software_run_get_version : os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files/software/second'),
				SoftwareTest.KEY_version : '0.3',
				SoftwareTest.KEY_version_major_number : SoftwareTest.KEY_version_pass_equal_or_bigger,
				SoftwareTest.KEY_version_minor_number : SoftwareTest.KEY_version_pass_equal_or_bigger,
			}
		
		self.assertTrue(software_test.test_software(SOFTWARE_test_1))
		self.assertFalse(software_test.test_software(SOFTWARE_test_2))
		self.assertFalse(software_test.test_software(SOFTWARE_test_3))
		self.assertTrue(software_test.test_software(SOFTWARE_test_4))
		self.assertFalse(software_test.test_software(SOFTWARE_test_5))
		self.assertTrue(software_test.test_software(SOFTWARE_test_6))
	
	
	def test_software_third(self):
		"""
		output: "version: version"
		"""
		
		software_test = SoftwareTest()
		SOFTWARE_test_1 = { 
				SoftwareTest.KEY_software_name : 'third',
				SoftwareTest.KEY_software_run : os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files/software/third'),
				SoftwareTest.KEY_software_run_get_version : os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files/software/third'),
				SoftwareTest.KEY_version : '1.5',
				SoftwareTest.KEY_version_major_number : SoftwareTest.KEY_version_pass_equal,
				SoftwareTest.KEY_version_minor_number : SoftwareTest.KEY_version_pass_equal_or_bigger,
			}
		
		self.assertEqual(None, self.assertFalse(software_test.test_software(SOFTWARE_test_1)))
		
	def test_software_fourth(self):
		"""
		output: "2.17-r974-dirty"
		"""
		
		software_test = SoftwareTest()
		SOFTWARE_test_1 = { 
				SoftwareTest.KEY_software_name : 'fourth',
				SoftwareTest.KEY_software_run : os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files/software/fourth'),
				SoftwareTest.KEY_software_run_get_version : os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files/software/fourth'),
				SoftwareTest.KEY_version : '2.17',
				SoftwareTest.KEY_version_major_number : SoftwareTest.KEY_version_pass_equal,
				SoftwareTest.KEY_version_minor_number : SoftwareTest.KEY_version_pass_equal_or_bigger,
			}
		
		self.assertTrue(software_test.test_software(SOFTWARE_test_1))
		
	def test_software_fourth_error(self):
		"""
		output: "2.17-r974-dirty"
		"""
		
		software_test = SoftwareTest()
		SOFTWARE_test_1 = { 
				SoftwareTest.KEY_software_name : 'fourth',
				SoftwareTest.KEY_software_run : os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files/software/fourth'),
				SoftwareTest.KEY_software_run_get_version : os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files/software/fourth_error'),
				SoftwareTest.KEY_version : '2.17',
				SoftwareTest.KEY_version_major_number : SoftwareTest.KEY_version_pass_equal,
				SoftwareTest.KEY_version_minor_number : SoftwareTest.KEY_version_pass_equal_or_bigger,
			}
		
		try:
			software_test.test_software(SOFTWARE_test_1)
		except Exception as e:
			self.assertEqual("Error: software '{}' is not present in your PATH".format(\
				SOFTWARE_test_1[SoftwareTest.KEY_software_name]), str(e))

	def test_all_software(self):
		"""
		test all software
		"""
		
		software = Software()
		try:
			software.test_softwares()
		except Exception as e:
			self.fail(str(e))







