import csv


class FoodMaterialImportService():
	@staticmethod
	def run(file):
		param = file.read().decode('utf8')
		data  = csv.DictReader(param, delimiter=',', quotechar='"')
		for row in data:
			print(next (iter (row.values())))
