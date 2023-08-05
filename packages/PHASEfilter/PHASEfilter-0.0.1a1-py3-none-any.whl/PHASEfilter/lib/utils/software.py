'''
Created on 12/12/2019

@author: mmp
'''

from PHASEfilter.lib.utils.testing_software import SoftwareTest
	
class Software(SoftwareTest):
	'''
	All extra software used in the application
	'''

	SOFTWARE_blast_name = 'blastn'
	SOFTWARE_blast = { 
					SoftwareTest.KEY_software_name : SOFTWARE_blast_name,
					SoftwareTest.KEY_software_run : 'blastn',
					SoftwareTest.KEY_software_run_get_version : 'blastn -version', 
					SoftwareTest.KEY_version : '2.3',
					SoftwareTest.KEY_version_major_number : SoftwareTest.KEY_version_pass_equal,
					SoftwareTest.KEY_version_minor_number : SoftwareTest.KEY_version_pass_equal_or_bigger,
				}
	
	SOFTWARE_minimap2_name = 'minimap2'
	SOFTWARE_minimap2 = { 
					SoftwareTest.KEY_software_name : SOFTWARE_minimap2_name, 
					SoftwareTest.KEY_software_run : 'minimap2', 
					SoftwareTest.KEY_software_run_get_version : 'minimap2 --version', 
					SoftwareTest.KEY_version : '2.0',
					SoftwareTest.KEY_version_major_number : SoftwareTest.KEY_version_pass_equal,
					SoftwareTest.KEY_version_minor_number : SoftwareTest.KEY_version_pass_equal_or_bigger,
				}
	
	SOFTWARE_lastz_name = 'lastz'
	SOFTWARE_lastz = {
					SoftwareTest.KEY_software_name : SOFTWARE_lastz_name, 
					SoftwareTest.KEY_software_run : 'lastz', 
					SoftwareTest.KEY_software_run_get_version : 'lastz --version', 
					SoftwareTest.KEY_version : '1.4',
					SoftwareTest.KEY_version_major_number : SoftwareTest.KEY_version_pass_equal,
					SoftwareTest.KEY_version_minor_number : SoftwareTest.KEY_version_pass_equal_or_bigger,
				}
		
	SOFTWARE_bcftools_name = 'bcftools'
	SOFTWARE_bcftools = {
					SoftwareTest.KEY_software_name : SOFTWARE_bcftools_name, 
					SoftwareTest.KEY_software_run : 'bcftools', 
					SoftwareTest.KEY_software_run_get_version : 'bcftools --version', 
					SoftwareTest.KEY_version : '1.3',
					SoftwareTest.KEY_version_major_number : SoftwareTest.KEY_version_pass_equal,
					SoftwareTest.KEY_version_minor_number : SoftwareTest.KEY_version_pass_equal_or_bigger,
				}
	
	SOFTWARE_samtools_name = 'samtools' 
	SOFTWARE_samtools = {
					SoftwareTest.KEY_software_name : SOFTWARE_samtools_name, 
					SoftwareTest.KEY_software_run : 'samtools', 
					SoftwareTest.KEY_software_run_get_version : 'samtools --version', 
					SoftwareTest.KEY_version : '1.3',
					SoftwareTest.KEY_version_major_number : SoftwareTest.KEY_version_pass_equal,
					SoftwareTest.KEY_version_minor_number : SoftwareTest.KEY_version_pass_equal_or_bigger,
				}
	
	SOFTWARE_tabix_name = 'tabix'
	SOFTWARE_tabix = {
					SoftwareTest.KEY_software_name : SOFTWARE_tabix_name, 
					SoftwareTest.KEY_software_run : 'tabix', 
					SoftwareTest.KEY_software_run_get_version : 'tabix', 
					SoftwareTest.KEY_version : '1.3',
					SoftwareTest.KEY_version_major_number : SoftwareTest.KEY_version_pass_equal,
					SoftwareTest.KEY_version_minor_number : SoftwareTest.KEY_version_pass_equal_or_bigger,
				}
	
	SOFTWARE_bgzip_name = 'bgzip'
	SOFTWARE_bgzip = {
					SoftwareTest.KEY_software_name : SOFTWARE_bgzip_name, 
					SoftwareTest.KEY_software_run : 'bgzip', 
					SoftwareTest.KEY_software_run_get_version : 'bgzip --version', 
					SoftwareTest.KEY_version : '1.3',
					SoftwareTest.KEY_version_major_number : SoftwareTest.KEY_version_pass_equal,
					SoftwareTest.KEY_version_minor_number : SoftwareTest.KEY_version_pass_equal_or_bigger,
				}
	
	### all software that is going to be tested
	VECT_SOFTWARE_TO_TEST = [SOFTWARE_minimap2,\
			SOFTWARE_blast,\
			SOFTWARE_bcftools, SOFTWARE_samtools, \
			SOFTWARE_tabix, SOFTWARE_bgzip, \
			SOFTWARE_lastz]
	
	### software that make the alignment
	VECT_SOFTWARE_DO_ALIGNMENT = [\
				SOFTWARE_minimap2[SoftwareTest.KEY_software_name],\
				SOFTWARE_lastz[SoftwareTest.KEY_software_name],\
				SOFTWARE_blast[SoftwareTest.KEY_software_name],\
				]


	def __init__(self):
		'''
		Constructor
		'''
		pass


	def get_bcf_tools(self):
		"""
		:out bcftools application to run in OS
		"""
		return self.SOFTWARE_bcftools[SoftwareTest.KEY_software_run]
	
	def get_tabix(self):
		return self.SOFTWARE_tabix[SoftwareTest.KEY_software_run]
	
	def get_bgzip(self):
		return self.SOFTWARE_bgzip[SoftwareTest.KEY_software_run]
	
	def get_samtools(self):
		return self.SOFTWARE_samtools[SoftwareTest.KEY_software_run]
	
	def get_blast(self):
		return self.SOFTWARE_blast[SoftwareTest.KEY_software_run]

	def get_minimap2(self):
		return self.SOFTWARE_minimap2[SoftwareTest.KEY_software_run]
	
	def get_lastz(self):
		return self.SOFTWARE_lastz[SoftwareTest.KEY_software_run]
	
	def get_application(self, app_name):
		"""
		:param name of applciation to return
		:out application to run in OS
		"""
		for software in self.VECT_SOFTWARE_TO_TEST:
			if software[SoftwareTest.KEY_software_name] == app_name:
				return software[SoftwareTest.KEY_software_run]
		raise Exception("Error: could not find this software '{}' in available softwares.".format(app_name))

	def test_softwares(self):
		"""
		test all software, if fails exit the application
		"""
		
		for software in self.VECT_SOFTWARE_TO_TEST:
			result = self.test_software(software)
			if result:
				print("Software: '{}' version: '{}' is OK".format(
					software[Software.KEY_software_name], software[Software.KEY_version]))
			else:
				raise Exception("Error: software '{}' has a lower version than '{}'".format(
					software[Software.KEY_software_name], software[Software.KEY_version]))

	def print_all(self):
		"""
		print a list of a software need
		"""
		print("Software{: <10}version".format(" "))
		for software in self.VECT_SOFTWARE_TO_TEST:
			print("{: <18}{}".format(
				software[Software.KEY_software_name], software[Software.KEY_version]))
			
if __name__ == '__main__':
	
	software = Software()
	software.print_all()

