import csv


class CSVHandler:
	def __init__(self,file_name,header):
		self.output_data = []	# This was originally a dict {}
		self.file_name = file_name
		self.header = header
		self.root_path = r'C:\Users\andre\Documents\MEGA\Work\Pacific West Land\\'
		self.make_output_file()


	def make_output_file(self):
		# Load up data from Raw BitMEX csv
		print("Making CSV output file....")
		with open(self.root_path + self.file_name + '.csv', 'w', newline='') as csvfile:
			writer = csv.writer(csvfile)
			writer.writerow(self.header)

		csvfile.close()
		print("Output File created with header.")

	def append_output_file(self, data_to_append):
		# open the file in "append" mode
		with open(self.root_path + self.file_name + '.csv', 'a', newline='') as csvfile:
			writer = csv.writer(csvfile)
			for row in data_to_append:
				writer.writerow(row)

		csvfile.close()
		print("Finished appending output file.")
