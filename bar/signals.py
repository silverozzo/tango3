from django.db.models.signals import pre_save, pre_delete
from django.dispatch          import receiver

from bar.models import FoodMaterialItem, FoodMaterialSpend
from bar.models import FoodMaterialCachedRest


@receiver(pre_save, sender=FoodMaterialItem)
def food_material_item_changing_handler(sender, **kwargs):
	FoodMaterialCachedRest.clear_from(
			kwargs['instance'].food_material, 
			kwargs['instance'].when
		)


@receiver(pre_save, sender=FoodMaterialSpend)
def food_material_spend_changing_handler(sender, **kwargs):
	FoodMaterialCachedRest.clear_from(
			kwargs['instance'].food_material, 
			kwargs['instance'].when
		)


@receiver(pre_delete, sender=FoodMaterialItem)
def food_material_item_delete_handler(sender, **kwargs):
	FoodMaterialCachedRest.clear_from(
			kwargs['instance'].food_material, 
			kwargs['instance'].when
		)


@receiver(pre_delete, sender=FoodMaterialSpend)
def food_material_spend_delete_handler(sender, **kwargs):
	FoodMaterialCachedRest.clear_from(
			kwargs['instance'].food_material, 
			kwargs['instance'].when
		)
