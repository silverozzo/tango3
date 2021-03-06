from datetime    import datetime
from decimal     import Decimal, getcontext
from django.test import TestCase

from .models import WorkDay, Account, AccountTransaction
from .models import FoodMaterial, FoodMaterialItem, FoodMaterialSpend
from .models import FoodMaterialCachedRest
from .models import Recipe, RecipeIngredient, Calculation


def work_day_creating(date=datetime.now().date()):
	day = WorkDay(date=date)
	day.save()
	
	return day


def work_day_current_creating(date=datetime.now().date()):
	day = work_day_creating(date)
	day.is_current = True
	day.save()
	
	return day


def food_material_creating(name='foobar'):
	material = FoodMaterial(name=name)
	material.save()
	return material


def food_material_item_creating(material, day, cost=Decimal('1.0')):
	item = FoodMaterialItem(
		food_material = material, 
		when          = day, 
		cost          = cost, 
		count         = Decimal('1.0'),
		rest          = Decimal('1.0')
	)
	item.save()
	return item


def food_material_spend_creating(material, day, transaction, count=Decimal('0.5')):
	spend = FoodMaterialSpend(
		food_material = material,
		when          = day,
		count         = count,
		transaction   = transaction,
	)
	spend.save()
	return spend


def recipe_creating(name='foobar'):
	recipe = Recipe(name=name)
	recipe.save()
	return recipe


def recipe_ingredient_creating(recipe, material):
	ingredient = RecipeIngredient(
		recipe        = recipe,
		food_material = material,
		count         = Decimal('0.01')
	)
	ingredient.save()
	return ingredient


def account_creating():
	account = Account();
	account.save()
	return account


def transaction_creating(account, day):
	transaction = AccountTransaction(
		account = account,
		day     = day,
		summ    = Decimal(1)
	)
	transaction.save()
	return transaction


class WorkDayTests(TestCase):
	def test_simple_day_creating(self):
		day = work_day_creating()
		self.assertEqual(False, day.is_current)
	
	def test_current_day_creating(self):
		day = work_day_current_creating()
		self.assertEqual(True, day.is_current)
	
	def test_current_changing(self):
		first  = work_day_current_creating()
		second = work_day_current_creating()
		first.refresh_from_db()
		
		self.assertEqual(False, first.is_current)
		self.assertEqual(True, second.is_current)
	
	def test_get_current_day(self):
		first  = work_day_current_creating()
		second = work_day_creating()
		check  = WorkDay.get_current()
		self.assertEqual(check, first)
		self.assertNotEqual(check, second)


class FoodMaterialTests(TestCase):
	def test_simple_material_creating(self):
		material = food_material_creating('foo')
		self.assertEqual('foo', material.name)
	
	def test_material_with_item_creating(self):
		material   = food_material_creating('foo')
		null_day   = work_day_creating('2016-02-10')
		first_day  = work_day_creating('2016-02-20')
		second_day = work_day_creating('2016-02-22')
		third_day  = work_day_creating('2016-02-24')
		first      = food_material_item_creating(material, first_day)
		second     = food_material_item_creating(material, second_day)
		
		first.cost = 10
		first.save()
		second.cost = 20
		second.save()
		
		self.assertEqual(0, material.get_cost(null_day.date))
		self.assertEqual(10, material.get_cost(first_day.date))
		self.assertEqual(20, material.get_cost(second_day.date))
		self.assertEqual(20, material.get_cost(third_day.date))
	
	def test_small_item_cost(self):
		material = food_material_creating()
		day      = work_day_creating()
		item     = food_material_item_creating(material, day)
		item.cost  = Decimal('0.01')
		item.count = Decimal('10.0')
		item.save()
		
		self.assertEqual(Decimal('0.01'), item.unit_cost)
	
	def test_empty_rest(self):
		material = food_material_creating()
		day      = work_day_creating()
		self.assertEqual(Decimal(0), material.get_rest(day))
	
	def test_simple_rest(self):
		material = food_material_creating()
		day      = work_day_creating()
		food_material_item_creating(material, day)
		food_material_item_creating(material, day)
		self.assertEqual(Decimal(2), material.get_rest(day))
	
	def test_simple_cached_rest(self):
		material = food_material_creating()
		day      = work_day_creating()
		food_material_item_creating(material, day)
		
		rest = FoodMaterialCachedRest.get_count(material, day)
		self.assertEqual(Decimal(1), rest)
	
	def test_cached_rest_from_yestarday(self):
		material = food_material_creating()
		day1     = work_day_creating('2016-03-01')
		food_material_item_creating(material, day1)
		day2     = work_day_creating('2016-03-02')
		food_material_item_creating(material, day2)
		
		rest = FoodMaterialCachedRest.get_count(material, day1)
		self.assertEqual(Decimal(1), rest)
		
		rest = FoodMaterialCachedRest.get_count(material, day2)
		self.assertEqual(Decimal(2), rest)

	def test_cached_rest_with_spend(self):
		material    = food_material_creating()
		day         = work_day_creating('2016-03-01')
		account     = account_creating()
		transaction = transaction_creating(account, day)
		
		food_material_item_creating(material, day)
		food_material_spend_creating(material, day, transaction)
		
		rest = FoodMaterialCachedRest.get_count(material, day)
		self.assertEqual(Decimal('0.5'), rest)
	
	def test_autoclear_cached_rest(self):
		material = food_material_creating()
		day      = work_day_creating()
		
		check = FoodMaterialCachedRest.objects.all().count()
		self.assertEqual(0, check)
		rest = FoodMaterialCachedRest.get_count(material, day)
		self.assertEqual(Decimal(0), rest)
		check = FoodMaterialCachedRest.objects.all().count()
		self.assertEqual(1, check)
		
		food_material_item_creating(material, day)
		
		check = FoodMaterialCachedRest.objects.all().count()
		self.assertEqual(0, check)
		rest = FoodMaterialCachedRest.get_count(material, day)
		self.assertEqual(Decimal(1), rest)
		check = FoodMaterialCachedRest.objects.all().count()
		self.assertEqual(1, check)


class CalculationTests(TestCase):
	def test_simple_drink(self):
		day = work_day_current_creating()
		mat = food_material_creating('mat1')
		mat.unit_name = 'unit name'
		mat.save()
		
		mat_item = food_material_item_creating(mat, day)
		recipe   = recipe_creating()
		ingr     = recipe_ingredient_creating(recipe, mat)
		calc     = Calculation.create(ingr)
		
		self.assertEqual(calc.when_date,       day.date)
		self.assertEqual(calc.what_name,       mat.name)
		self.assertEqual(calc.what_unit_cost,  mat_item.unit_cost)
		self.assertEqual(calc.what_count,      ingr.count)
		self.assertEqual(calc.what_unit_name,  mat.unit_name)
		self.assertEqual(calc.on_prescription, recipe)
	
	def test_change_costs(self):
		day      = work_day_current_creating()
		mat      = food_material_creating('mat1')
		mat_item = food_material_item_creating(mat, day)
		recipe   = recipe_creating()
		ingr     = recipe_ingredient_creating(recipe, mat)
		calc     = Calculation.create(ingr)
		
		self.assertEqual(1, Calculation.objects.count())
		self.assertEqual(Decimal('0.01'), calc.what_full_cost)
		
		mat_item.cost = Decimal('2.00')
		mat_item.save()
		calc = Calculation.create(ingr)
		
		self.assertEqual(1, Calculation.objects.count())
		self.assertEqual(Decimal('0.02'), calc.what_full_cost)
