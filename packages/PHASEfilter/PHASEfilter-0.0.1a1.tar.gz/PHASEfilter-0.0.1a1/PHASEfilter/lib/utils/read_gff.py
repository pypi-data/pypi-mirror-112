'''
Created on 02/12/2020

@author: mmp
'''
from gff3tool.lib.gff3 import Gff3
from PHASEfilter.lib.utils.util import Utils

class ReadGFF(object):
	'''
	classdocs
	'''
	PROCESS_TYPE_all = "ALL"

	def __init__(self, file_name):
		'''
		Constructor
		'''
		self.file_name = file_name
		self.utils = Utils()
		
	def parse_gff(self, file_result, vect_type_to_process, vect_pass_ref, lift_over_ligth):
		"""
		:param file_result - output file
		:param vect_type_to_process - name of the type to process or PROCESS_TYPE
		:param lift_over_ligth - method to pass, ref_a is always the main reference
		:out line processed
		"""
		chr_name = ""	### nothing processed yet
		vect_fail_synch = []
		(lines_parsed, lines_failed_parse) = (0, 0)
		with open(self.file_name) as handle_read, open(file_result, 'w') as handle_out:
			gff = Gff3(handle_read)
			for line_gff in gff.lines:
				## {'line_index': 34, 'line_raw': 'chrI\tS01\tTY1/TY2_soloLTR\t36933\t37200\t.\t+\t.\tID=TY1/TY2_soloLTR:chrI:36933-37200:+;Name=TY1/TY2_soloLTR:chrI:36933-37200:+\n', 
				## 'line_status': 'normal', 'parents': [], 'children': [], 'line_type': 'feature', 'directive': '', 'line_errors': [], 'type': 'TY1/TY2_soloLTR', 'seqid': 'chrI', 'source': 'S01', 'start': 36933, 'end': 37200, 'score': '.', 'strand': '+', 'phase': '.', 
				## 'attributes': {'ID': 'TY1/TY2_soloLTR:chrI:36933-37200:+', 'Name': 'TY1/TY2_soloLTR:chrI:36933-37200:+'}}
				
				fail_get_position = True
				if line_gff['line_type'] == 'feature' and (line_gff['type'] in vect_type_to_process or\
					ReadGFF.PROCESS_TYPE_all in vect_type_to_process):

					### if failed synch save line and continue
					if (line_gff["seqid"].lower() in vect_fail_synch):
						handle_out.write(line_gff["line_raw"])
						continue
				
					## test chr_name					
					if (chr_name != line_gff["seqid"]):
						chr_name = line_gff["seqid"]
						if (chr_name.lower() in vect_pass_ref): continue	### chr to not process
						if (not lift_over_ligth.synchronize_sequences(chr_name, chr_name)):
							handle_out.write(line_gff["line_raw"])
							vect_fail_synch.append(chr_name)
							continue
					
					### test positions
					(result_start, result_end) = (-1, -1)
					if (self.utils.is_integer(line_gff['start']) and self.utils.is_integer(line_gff['end'])):
						### parse positions
						(result_start, result_most_left_start) = lift_over_ligth.get_best_pos_in_target(chr_name, chr_name, int(line_gff['start']))
						if (result_start != -1): fail_get_position = False
						
						if (result_start != -1):
							(result_end, result_most_left_end) = lift_over_ligth.get_best_pos_in_target(chr_name, chr_name, int(line_gff['end']))
							if (result_end == -1): fail_get_position = True
						
					### save new position
					if (not fail_get_position and result_start != -1 and result_end != -1):
						handle_out.write(line_gff["line_raw"].strip() + ";StartHit={};EndHit={}\n".format(
							result_start, result_end))
						lines_parsed += 1
					else:
						handle_out.write(line_gff["line_raw"])
						lines_failed_parse += 1
				else:
					handle_out.write(line_gff["line_raw"])
		
		return (lines_parsed, lines_failed_parse, vect_fail_synch)


