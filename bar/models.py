from django.db import models


class WorkDay(models.Model):
	date = models.DateField()

	def __str__(self):
		return str(self.date)


class FoodMaterial(models.Model):
	name = models.CharField(max_length=200)
	
	def __str__(self):
		return self.name


class FoodMaterialItem(models.Model):
	food_material = models.ForeignKey(FoodMaterial)
	when          = models.ForeignKey(WorkDay)
	cost          = models.DecimalField(max_digits=8, decimal_places=2)
	count         = models.DecimalField(max_digits=8, decimal_places=4)
	
	def __str__(self):
		return str(self.food_material) + '(' + str(self.when) + ')'


class Receipt(models.Model):
	name    = models.CharField(max_length=200)
	comment = models.TextField()
	
	def __str__(self):
		return self.name


class ReceiptIngredient(models.Model):
	receipt       = models.ForeignKey(Receipt)
	food_material = models.ForeignKey(FoodMaterial)
	extra_action  = models.TextField()
	count         = models.DecimalField(max_digits=8, decimal_places=4)
	
	def __str__(self):
		return str(self.food_material) + ' x ' + str(self.count)


class Product(models.Model):
	name    = models.CharField(max_length=200)
	receipt = models.OneToOneField(Receipt)
	
	def __str__(self):
		return self.name
