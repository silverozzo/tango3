from django.db                  import models
from django.db.models           import Sum
from django.db.models.functions import Coalesce

import decimal
import math


class WorkDay(models.Model):
	date       = models.DateField()
	is_current = models.BooleanField(default=False)
	
	class Meta:
		ordering = ['-date']
	
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
	unit_name = models.CharField(max_length=200, blank=True, default='')
	
	class Meta:
		ordering = ['name']
	
	def __unicode__(self):
		return self.name
	
	def __str__(self):
		return self.name
	
	def get_item(self, date):
		item = FoodMaterialItem.objects.filter(food_material=self, when__date__lte=date)
		if not item.exists():
			return None
		
		return item.order_by('-when__date')[0]
	
	def get_item_with_rest(self):
		item = FoodMaterialItem.objects.filter(food_material=self, rest__gt=0)
		if not item.exists():
			return None
		
		return item.order_by('when__date')[0]
	
	def get_cost(self, date):
		item = self.get_item(date)
		if not item:
			return decimal.Decimal(0)
		
		return item.unit_cost
	
	def get_rest(self):
		result = FoodMaterialItem.objects.filter(food_material=self, rest__gt=0).aggregate(Sum('rest'))
		if result['rest__sum'] is None:
			return decimal.Decimal(0)
		return result['rest__sum']
	
	def get_spend(self):
		result = FoodMaterialSpend.objects.filter(food_material=self, count__gt=0).aggregate(Sum('count'))
		if result['count_sum'] is None:
			return decimal.Decimal(0)
		return result['count_sum']
	
	def make_spend(self, count, transaction):
		rest = count
		for item in FoodMaterialItem.objects.filter(food_material=self, rest__gt=0).order_by('when__date'):
			if rest <= decimal.Decimal(0):
				break
			
			if item.rest >= rest:
				item.rest -= rest
				item.save()
				rest = decimal.Decimal(0)
				continue
			
			if item.rest < rest:
				rest -= item.rest
				item.rest = decimal.Decimal(0)
				item.save()
				continue
		
		FoodMaterialSpend.create(self, transaction, count - rest)


class FoodMaterialItem(models.Model):
	food_material = models.ForeignKey(FoodMaterial)
	when          = models.ForeignKey(WorkDay)
	cost          = models.DecimalField(max_digits=8, decimal_places=2)
	count         = models.DecimalField(max_digits=8, decimal_places=4)
	rest          = models.DecimalField(max_digits=8, decimal_places=4, default=0)
	unit_cost     = models.DecimalField(max_digits=8, decimal_places=2, default=0)
	
	class Meta():
		ordering = ['-when__date']
	
	def __unicode__(self):
		return unicode(self.food_material) + ' (' + str(self.when) + ')'
	
	def __str__(self):
		return unicode(self.food_material) + ' (' + str(self.when) + ')'
	
	def save(self, *args, **kwargs):
		self.unit_cost = decimal.Decimal(self.cost) / decimal.Decimal(self.count)
		self.unit_cost = self.unit_cost.quantize(self.cost, rounding=decimal.ROUND_UP)
		
		if not self.pk and self.rest is None:
			self.rest = self.count
		
		return super(FoodMaterialItem, self).save(*args, **kwargs)


class Recipe(models.Model):
	name    = models.CharField(max_length=200)
	comment = models.TextField(blank=True)
	process = models.TextField(blank=True)
	
	class Meta:
		ordering = ['name']
	
	def __unicode__(self):
		return self.name
	
	def __str__(self):
		return self.name


class RecipeIngredient(models.Model):
	recipe        = models.ForeignKey(Recipe)
	food_material = models.ForeignKey(FoodMaterial)
	extra_action  = models.CharField(max_length=250, blank=True)
	count         = models.DecimalField(max_digits=8, decimal_places=4)
	
	def __unicode__(self):
		return unicode(self.food_material) + ' x ' + str(self.count)
	
	def __str__(self):
		return unicode(self.food_material) + ' x ' + str(self.count)


class Calculation(models.Model):
	when_date       = models.DateField()
	what_name       = models.CharField(max_length=200)
	what_unit_cost  = models.DecimalField(max_digits=8, decimal_places=2)
	what_count      = models.DecimalField(max_digits=8, decimal_places=4)
	what_unit_name  = models.CharField(max_length=200)
	what_full_cost  = models.DecimalField(max_digits=8, decimal_places=2)
	feasible        = models.BooleanField(default=False)
	on_prescription = models.ForeignKey(Recipe)
	on_ingredient   = models.ForeignKey(RecipeIngredient, default=None)
	
	@staticmethod
	def create(ingredient):
		work_day = WorkDay.get_current()
		Calculation.objects.filter(
				when_date     = work_day.date, 
				on_ingredient = ingredient).delete()
		
		calculation = Calculation()
		calculation.when_date       = work_day.date
		calculation.what_name       = ingredient.food_material.name
		calculation.what_unit_cost  = ingredient.food_material.get_cost(work_day.date)
		calculation.what_count      = ingredient.count
		calculation.what_unit_name  = ingredient.food_material.unit_name
		calculation.on_prescription = ingredient.recipe
		calculation.on_ingredient   = ingredient
		calculation.feasible        = ingredient.food_material.get_rest() >= ingredient.count
		calculation.save()
		
		return calculation
	
	def save(self, *args, **kwargs):
		self.what_full_cost = self.what_unit_cost * self.what_count
		self.what_full_cost = self.what_full_cost.quantize(decimal.Decimal('.01'), rounding=decimal.ROUND_UP)
		
		return super(Calculation, self).save(*args, **kwargs)


class Product(models.Model):
	name        = models.CharField(max_length=200)
	recipe      = models.OneToOneField(Recipe)
	fixed_price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
	rounding    = models.DecimalField(max_digits=8, decimal_places=2, default=1)
	markup      = models.DecimalField(max_digits=8, decimal_places=2, default=1)
	is_active   = models.BooleanField(default=True)
	
	def __unicode__(self):
		return self.name
	
	def __str__(self):
		return self.name
	
	def make_price(self, cost):
		price = (cost * self.markup) / (decimal.Decimal(10)**self.rounding)
		price = price.quantize(decimal.Decimal('1'), rounding=decimal.ROUND_UP)
		price = price * (decimal.Decimal(10)**self.rounding)
		
		if self.fixed_price > price:
			price = self.fixed_price
		if price > self.fixed_price:
			print('calculated price is more than fixed')
		
		return price


class SaleOffer(models.Model):
	product  = models.ForeignKey(Product)
	day      = models.ForeignKey(WorkDay)
	cost     = models.DecimalField(max_digits=8, decimal_places=2, default=decimal.Decimal('0.00'))
	price    = models.DecimalField(max_digits=8, decimal_places=2, default=decimal.Decimal('0.00'))
	feasible = models.BooleanField(default=False)
	
	class Meta:
		ordering = ('product__name',)
	
	def __unicode__(self):
		return unicode(self.product) + ' (' + str(self.day) + ') -- ' + str(self.price)
	
	def __str__(self):
		return unicode(self.product) + ' (' + str(self.day) + ') -- ' + str(self.price)
	
	def save(self, *args, **kwargs):
		cost     = decimal.Decimal('0.00')
		price    = decimal.Decimal('0.00')
		feasible = True
		
		ingredients = RecipeIngredient.objects.filter(recipe=self.product.recipe)
		for ingredient in ingredients:
			calculation = Calculation.create(ingredient)
			cost += calculation.what_full_cost
			
			if not calculation.feasible:
				feasible = False
		
		self.cost     = cost
		self.price    = self.product.make_price(cost)
		self.feasible = feasible
		
		return super(SaleOffer, self).save(*args, **kwargs)
	
	@staticmethod
	def generate():
		day = WorkDay.get_current()
		existed = SaleOffer.objects.filter(day=day).values_list('product', flat=True)
		
		for product in Product.objects.filter(is_active=True):
			if product.id in existed:
				continue
			
			offer = SaleOffer(
				product = product,
				day     = day
			)
			offer.save()


class Account(models.Model):
	name       = models.CharField(max_length=200)
	is_default = models.BooleanField(default=False)
	costed     = models.BooleanField(default=False)
	
	def __unicode__(self):
		return self.name


class AccountTransaction(models.Model):
	account    = models.ForeignKey(Account)
	day        = models.ForeignKey(WorkDay)
	sale_offer = models.ForeignKey(SaleOffer, blank=True, default=None)
	summ       = models.DecimalField(max_digits=8, decimal_places=2, blank=True)
	mod_half   = models.BooleanField(default=False)
	
	class Meta:
		ordering = ('-day',)
	
	def __unicode__(self):
		return unicode(self.sale_offer.product) + ' for ' + str(self.summ)
	
	def save(self, *args, **kwargs):
		if self.summ is None or self.summ == 0:
			if self.account.costed:
				self.summ = self.sale_offer.cost
			else:
				self.summ = self.sale_offer.price
		
		if self.mod_half:
			self.summ = self.summ / decimal.Decimal(2)
		
		need_spend = False
		if not self.pk:
			need_spend = True
		
		super(AccountTransaction, self).save(*args, **kwargs)
		
		if need_spend:
			ingredients = RecipeIngredient.objects.filter(recipe=self.sale_offer.product.recipe)
			for ingredient in ingredients:
				ingredient.food_material.make_spend(ingredient.count, self)
	
	@staticmethod
	def get_totals(day):
		return AccountTransaction.objects.filter(day=day).values('account', 'account__name', 'day').annotate(summ=Sum('summ'))


class FoodMaterialSpend(models.Model):
	food_material = models.ForeignKey(FoodMaterial)
	transaction   = models.ForeignKey(AccountTransaction)
	count         = models.DecimalField(max_digits=8, decimal_places=4)
	when          = models.ForeignKey(WorkDay)
	
	def __unicode__(self):
		return unicode(self.food_material) + ' x ' + str(self.count) + ' (' + str(self.when) + ')'
	
	@staticmethod
	def create(material, transaction, count):
		spend = FoodMaterialSpend()
		spend.food_material = self
		spend.transaction   = transaction
		spend.count         = count
		spend.when          = transaction.day
		spend.save()
