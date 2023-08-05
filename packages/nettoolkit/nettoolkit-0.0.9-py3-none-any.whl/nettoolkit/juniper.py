
# ------------------------------------------------------------------------------
from .gpl import STR, IO
from .hierarchy import Hierarchy 
from .jset import JSet
# ------------------------------------------------------------------------------

class Juniper():

	def __init__(self, input_file, output_file=None):
		self.input_file = input_file
		self.output_file = output_file

	def _get_clean_output_file_lst(self):
		output_file_lst = []
		for line in self.input_file_lst:
			if line.lstrip()[0] == "#": continue
			output_file_lst.append(line.rstrip("\n"))
		return output_file_lst

	def remove_remarks(self, to_file=True):
		self.input_file_lst = IO.file_to_list(self.input_file)
		output_file_lst = self._get_clean_output_file_lst()
		if to_file and self.output_file:
			IO.to_file(self.output_file, output_file_lst)
		return output_file_lst

	def convert_to_set(self, to_file=True):
		J = JSet(self.input_file)
		J.to_set
		if to_file and self.output_file:
			IO.to_file(self.output_file, J.output)
		return J.output

	def convert_to_hierarchy(self, to_file=True):
		H = Hierarchy(self.input_file, self.output_file)
		H.convert()
		if to_file and self.output_file:
			IO.to_file(self.output_file, H.output)
		return H.output


# ------------------------------------------------------------------------------
if __name__ == '__main__':
	pass
# ------------------------------------------------------------------------------
