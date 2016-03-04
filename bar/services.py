import datetime, decimal

from .models import WorkDay, FoodMaterial, FoodMaterialItem


class FoodMaterialImportService():
	messages = []
	
	@staticmethod
	def run(file):
		param = file.read().decode('utf-8').split("\r\n")[1:]
		for row in param:
			chunks = row.split("\t")
			if len(chunks) <= 0 or not chunks[1]:
				continue
			
			unit_name = ''
			if len(chunks) >= 5 and chunks[4]:
				unit_name = chunks[4]
			
			material = FoodMaterialImportService.get_food_material(chunks[1], unit_name)
			
			day = None
			if len(chunks) >= 8 and chunks[7]:
				day = FoodMaterialImportService.get_work_day(chunks[7])
				FoodMaterialImportService.check_item(material, day, chunks[2], chunks[3])
	
	@staticmethod
	def get_food_material(name, unit_name):
		if FoodMaterial.objects.filter(name=name).exists():
			return FoodMaterial.objects.get(name=name)
		
		material = FoodMaterial(name=name, unit_name=unit_name)
		material.save()
		
		return material
	
	@staticmethod
	def get_work_day(date_str):
		date_chunks = date_str.split('.')
		date = datetime.date(int(date_chunks[2]), int(date_chunks[1]), int(date_chunks[0]))
		if WorkDay.objects.filter(date=date).exists():
			return WorkDay.objects.get(date=date)
		
		day = WorkDay(date=date)
		day.save()
		
		return day
	
	@staticmethod
	def check_item(material, day, cost, count):
		FoodMaterialItem.objects.filter(food_material=material, when=day).delete()
		
		print(cost)
		cost  = decimal.Decimal( cost.replace(',', '.').replace(' ', '').replace(u'\xa0', ''))
		count = decimal.Decimal(count.replace(',', '.').replace(' ', '').replace(u'\xa0', ''))
		
		item = FoodMaterialItem(
			food_material = material,
			when          = day,
			cost          = cost,
			count         = count,
		)
		item.save()


class SimpleProductImportService():
	@staticmethod
	def run(file):
		param = file.read().decode('utf-8').split("\r\n")[1:]
		for row in param:
			pass
