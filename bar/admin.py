from django.contrib import admin

from .models import WorkDay, FoodMaterial, FoodMaterialItem, Recipe, RecipeIngredient, Calculation, Product, SaleOffer


class FoodMaterialItemInline(admin.TabularInline):
	model = FoodMaterialItem


class FoodMaterialAdmin(admin.ModelAdmin):
	list_display  = ('name', 'unit_name')
	list_editable = ['unit_name']
	inlines       = [FoodMaterialItemInline]


class RecipeIngredientInline(admin.TabularInline):
	model = RecipeIngredient


class RecipeAdmin(admin.ModelAdmin):
	inlines = [RecipeIngredientInline]


class CalculationAdmin(admin.ModelAdmin):
	list_display = ('when_date', 'on_prescription', 'what_name', 'what_unit_cost', 'what_count', 'what_unit_name', 'what_full_cost', 'on_ingredient')


admin.site.register(WorkDay)
admin.site.register(FoodMaterial, FoodMaterialAdmin)
admin.site.register(FoodMaterialItem)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredient)
admin.site.register(Product)
admin.site.register(Calculation, CalculationAdmin)
admin.site.register(SaleOffer)
