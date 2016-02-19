from django.contrib import admin

from .models import FoodMaterial, FoodMaterialItem, Product, Receipt, ReceiptIngredient, WorkDay


admin.register(WorkDay)
admin.register(FoodMaterial)
admin.register(FoodMaterialItem)
admin.register(Receipt)
admin.register(ReceiptIngredient)
admin.register(Product)
