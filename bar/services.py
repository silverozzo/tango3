import datetime, decimal

from .models import WorkDay, FoodMaterial, FoodMaterialItem
from .models import Recipe, RecipeIngredient, Product


def convert_to_money(strr):
	return decimal.Decimal(strr
			.replace(',', '.')
			.replace(' ', '')
			.replace(u'\xa0', '')
			.strip()
		)


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
			else:
				print('no item for material: ' + unicode(material))
	
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
		
		cost  = convert_to_money(cost)
		count = convert_to_money(count)
		
		item = FoodMaterialItem(
			food_material = material,
			when          = day,
			cost          = cost,
			count         = count,
		)
		item.save()


class SimpleProductImportService():
	messages = []
	
	@staticmethod
	def run(file, prefix):
		param = file.read().decode('utf-8').split("\r\n")[1:]
		for row in param:
			chunks = row.split("\t")
			if len(chunks) <= 0 or not chunks[1]:
				continue
			
			if not FoodMaterial.objects.filter(name=chunks[1]).exists():
				print('no material like: ' + chunks[1])
				continue
			
			product = SimpleProductImportService.get_product(chunks[1], 
				prefix, chunks[3], chunks[5], chunks[7])
	
	@staticmethod
	def get_product(name, prefix, ingredient_count, markup, fixed_price):
		check_name = prefix + ' ' + name
		
		if Product.objects.filter(name=check_name).exists():
			return Product.objects.get(name=check_name)
		
		recipe = SimpleProductImportService.get_recipe(name, prefix, ingredient_count)
		
		markup      = convert_to_money(markup)
		fixed_price = convert_to_money(fixed_price)
		
		product = Product(
			name        = check_name,
			recipe      = recipe,
			markup      = markup,
			fixed_price = fixed_price
		)
		product.save()
		
		return product
	
	@staticmethod
	def get_recipe(name, prefix, ingredient_count):
		check_name = prefix + ' ' + name
		
		if Recipe.objects.filter(name=check_name).exists():
			return Recipe.objects.get(name=check_name)
		
		recipe = Recipe(name=check_name)
		recipe.save()
		
		SimpleProductImportService.check_ingredient(name, recipe, ingredient_count)
		
		return recipe
	
	@staticmethod
	def check_ingredient(name, recipe, count):
		if RecipeIngredient.objects.filter(food_material__name=name, recipe=recipe).exists():
			return RecipeIngredient.objects.get(food_material__name=name, recipe=recipe)
		
		count = convert_to_money(count)
		
		material = FoodMaterial.objects.get(name=name) 
		ingr = RecipeIngredient(
			food_material = material,
			recipe        = recipe,
			count         = count
		)
		ingr.save()


class ComplexProductImportService():
	@staticmethod
	def run(file, prefix):
		param = file.read().decode('utf-8').split("\r\n")[1:]
		
		product = None
		line    = 0
		ingrs   = []
		counter = 1
		
		for row in param:
			chunks = row.split("\t")
			
			if chunks[0]:
				product = ComplexProductImportService.get_product(chunks[0], prefix)
				line    = 0
			
			if line == 1:
				for chunk in chunks[3:]:
					ingrs.append(chunk)
				ingrs.reverse()
			
			if line == 2:
				RecipeIngredient.objects.filter(
						recipe = product.recipe
					).delete()
				
				for chunk in chunks[3:]:
					name = ingrs.pop()
					
					if not name:
						continue
					
					if not FoodMaterial.objects.filter(name=name).exists():
						print('no food material on line ' + str(counter) + 
							': ' + str(name.encode('utf-8')))
						continue
					
					mat   = FoodMaterial.objects.get(name=name)
					count = convert_to_money(chunk)
					
					ingredient = RecipeIngredient(
						food_material = mat,
						recipe        = product.recipe,
						count         = count
					)
					
					ingredient.save()
			
			if line == 5 and chunks[2]:
				markup = convert_to_money(chunks[2])
				product.markup = markup
				product.save()
			
			if line == 6 and chunks[3]:
				fixed = convert_to_money(chunks[3])
				product.fixed_price = fixed
				product.save()
			
			if line == 7 and chunks[5]:
				product.recipe.process = chunks[5]
				product.recipe.save()
			
			line    += 1
			counter += 1
	
	@staticmethod
	def get_product(name, prefix):
		check_name = prefix + ' ' + name
		
		if Product.objects.filter(name=check_name).exists():
			return Product.objects.get(name=check_name)
		
		recipe = ComplexProductImportService.get_recipe(name, prefix)
		
		product = Product(
			name   = check_name,
			recipe = recipe
		)
		product.save()
		
		return product
	
	@staticmethod
	def get_recipe(name, prefix):
		check_name = prefix + ' ' + name
		
		if Recipe.objects.filter(name=check_name).exists():
			return Recipe.objects.get(name=check_name)
		
		recipe = Recipe(name=check_name)
		recipe.save()
		
		return recipe
