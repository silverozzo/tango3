from django.contrib import admin

from .models import WorkDay, FoodMaterial, FoodMaterialItem, Recipe, RecipeIngredient, Calculation, Product


admin.site.register(WorkDay)
admin.site.register(FoodMaterial)
admin.site.register(FoodMaterialItem)
admin.site.register(Recipe)
admin.site.register(RecipeIngredient)
admin.site.register(Product)
admin.site.register(Calculation)
