from django.db import models

import decimal
import math


class WorkDay(models.Model):
	date       = models.DateField()
	is_current = models.BooleanField(default=False)

	def __str__(self):
		return str(self.date)
	
	def save(self, *args, **kwargs):
		if self.is_current:
			WorkDay.objects.filter(is_current=True).update(is_current=False)
		return super(WorkDay, self).save(*args, **kwargs)
	
	@staticmethod
	def get_current():
		return WorkDay.objects.get(is_current=True)


class FoodMaterial(models.Model):
	name      = models.CharField(max_length=200)
	unit_name = models.CharField(max_length=200, default='')
	
	def __str__(self):
		return self.name
	
	def get_item(self, date):
		item = FoodMaterialItem.objects.filter(food_material=self, when__date__lte=date)
		if not item.exists():
			return None
		
		return item.order_by('-when__date')[0]
	
	def get_cost(self, date):
		item = self.get_item(date)
		if not item:
			return 0
		
		return item.unit_cost


class FoodMaterialItem(models.Model):
	food_material = models.ForeignKey(FoodMaterial)
	when          = models.ForeignKey(WorkDay)
	cost          = models.DecimalField(max_digits=8, decimal_places=2)
	count         = models.DecimalField(max_digits=8, decimal_places=4)
	rest          = models.DecimalField(max_digits=8, decimal_places=4, default=0)
	unit_cost     = models.DecimalField(max_digits=8, decimal_places=2, default=0)
	
	def __str__(self):
		return str(self.food_material) + ' (' + str(self.when) + ')'
	
	def save(self, *args, **kwargs):
		self.unit_cost = decimal.Decimal(self.cost) / decimal.Decimal(self.count)
		self.unit_cost = self.unit_cost.quantize(self.cost, rounding=decimal.ROUND_UP)
		
		return super(FoodMaterialItem, self).save(*args, **kwargs)


class Recipe(models.Model):
	name    = models.CharField(max_length=200)
	comment = models.TextField()
	
	def __str__(self):
		return self.name


class Calculation(models.Model):
	when_date       = models.DateField()
	what_name       = models.CharField(max_length=200)
	what_unit_cost  = models.DecimalField(max_digits=8, decimal_places=2)
	what_count      = models.DecimalField(max_digits=8, decimal_places=4)
	what_unit_name  = models.CharField(max_length=200)
	what_full_cost  = models.DecimalField(max_digits=8, decimal_places=2)
	on_prescription = models.ForeignKey(Recipe)
	
	def save(self, *args, **kwargs):
		decimal.getcontext().prec     = 2
		decimal.getcontext().rounding = decimal.ROUND_UP
		
		self.what_full_cost = self.what_unit_cost * self.what_count
		
		return super(Calculation, self).save(*args, **kwargs)


class RecipeIngredient(models.Model):
	recipe        = models.ForeignKey(Recipe)
	food_material = models.ForeignKey(FoodMaterial)
	extra_action  = models.TextField()
	count         = models.DecimalField(max_digits=8, decimal_places=4)
	
	def __str__(self):
		return str(self.food_material) + ' x ' + str(self.count)
	
	def make_calculation(self):
		work_day = WorkDay.get_current()
		
		Calculation.objects.filter(
				when_date       = work_day.date, 
				what_name       = self.food_material.name, 
				on_prescription = self.recipe).delete()
		
		calculation = Calculation()
		calculation.when_date       = work_day.date
		calculation.what_name       = self.food_material.name
		calculation.what_unit_cost  = self.food_material.get_cost(work_day.date)
		calculation.what_count      = self.count
		calculation.what_unit_name  = self.food_material.unit_name
		calculation.on_prescription = self.recipe
		calculation.save()
		
		return calculation


class Product(models.Model):
	name        = models.CharField(max_length=200)
	receipt     = models.OneToOneField(Recipe)
	fixed_price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
	
	def __str__(self):
		return self.name


class SaleOffer(models.Model):
	product = models.ForeignKey(Product)
	day     = models.ForeignKey(WorkDay)
	cost    = models.DecimalField(max_digits=8, decimal_places=2)
	price   = models.DecimalField(max_digits=8, decimal_places=2)
