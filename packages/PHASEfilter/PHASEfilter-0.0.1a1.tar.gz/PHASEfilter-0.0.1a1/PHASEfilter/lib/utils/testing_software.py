
import os

from PHASEfilter.lib.utils.util import Utils

class SoftwareTest(object):
	
	KEY_software_name = 'software_name'						## software name
	KEY_software_run = 'software_run'						## software calling by OS
	KEY_software_run_get_version = 'software_get_version'	## software calling by OS to get the version
	KEY_version = 'version'									## version required MAJOR.MINOR
	KEY_version_major_number = 'version_major_number' 		## if must be "equal" or "can be equal or greater"
	KEY_version_minor_number = 'version_minor_number'		## if must be "equal" or "can be equal or greater"
	KEY_version_pass_equal = 'equal'
	KEY_version_pass_equal_or_bigger = 'equal_or_bigger'
	
	#### utils
	utils = Utils()

	def __init__(self):
		pass
	
	def test_software(self, software):
		"""
		:param {'software' : <software to rum>, 'version' : <version string>}
		"""
		
		tmp_file = self.utils.get_temp_file('file_name', '.txt')
		cmd = "{} > {} 2>&1".format(software[SoftwareTest.KEY_software_run_get_version], tmp_file)
		exist_status = os.system(cmd)
		if (exist_status != 0 and exist_status != 256):
			self.utils.remove_file(tmp_file)
			raise Exception("Error: software '{}' is not present in your PATH".format(
					software[SoftwareTest.KEY_software_name]))
		
		### read file
		vect_data = self.utils.read_text_file(tmp_file)
		self.utils.remove_file(tmp_file)
		
		### 
		for line_ in vect_data:
			result = self.is_version_equal_or_bigger(line_, software)
			if (result is None): continue
			return result
		return None


	def is_version_equal_or_bigger(self, sz_string, software):
		"""
		:param string with possible version
			"blastn: 2.6.0+"
			"Package: blast 2.6.0, build Jan 15 2017 17:12:27"
			"2.17-r974-dirty"
			"2.17"
			
			Version "major.minor[.build[.revision]] (example: 1.2.12.102)"
		:out True -> is equal or bigger
		     False -> is less than version
		     None -> didn't found version in the string 
		"""
		(major_to_test, minor_to_test) = self.get_major_minor_version(software[SoftwareTest.KEY_version])
		if (major_to_test is None or minor_to_test is None): return None
		
		lst_data = sz_string.split()
		for string_to_test in lst_data:
			(major, minor) = self.get_major_minor_version(string_to_test)
			if (major is None or minor is None): continue
			else:		### test Version
				if (software[SoftwareTest.KEY_version_major_number] == SoftwareTest.KEY_version_pass_equal):
					if (major != major_to_test): return False
					if (software[SoftwareTest.KEY_version_minor_number] == SoftwareTest.KEY_version_pass_equal):
						if (minor != minor_to_test): return False
						return True
					else: 	## KEY_version_pass_equal_or_bigger
						if (minor < minor_to_test): return False
						return True
				else:	## KEY_version_pass_equal_or_bigger
					if (major < major_to_test): return False
					return True
		### didn't found anything
		return None


	def get_major_minor_version(self, version):
		"""
		get major and minor version from string
		:param "2.17-r974-dirty" or "blast"
		:out (None, None) if none found or (2,17) last string
		"""
		(major, minor) = (None, None)
		
		lst_data = version.split('.')
		if (len(lst_data) > 1):
			if (self.utils.is_integer(lst_data[0])): major = int(lst_data[0])
			if (self.utils.is_integer(lst_data[1])): minor = int(lst_data[1])
			else:
				lst_data_minor = lst_data[1].split("-")
				if (len(lst_data_minor) > 1 and self.utils.is_integer(lst_data_minor[0])):
					minor = int(lst_data_minor[0])
					
		if (major is None or minor is None): return (None, None)
		return (major, minor)
