from django.contrib import admin

from bar.models import WorkDay, FoodMaterial
from bar.models import FoodMaterialItem, FoodMaterialSpend, FoodMaterialCachedRest
from bar.models import Recipe, RecipeIngredient, Calculation, Product, SaleOffer, Account, AccountTransaction


class WorkDayAdmin(admin.ModelAdmin):
	list_display = ('date', 'is_current')


class FoodMaterialItemInline(admin.TabularInline):
	model = FoodMaterialItem


class FoodMaterialSpendInline(admin.TabularInline):
	model = FoodMaterialSpend


class FoodMaterialCachedRestInline(admin.TabularInline):
	model = FoodMaterialCachedRest


class FoodMaterialAdmin(admin.ModelAdmin):
	list_display  = ('name', 'unit_name')
	list_editable = ['unit_name']
	inlines       = [
			FoodMaterialItemInline, 
			FoodMaterialSpendInline,
			FoodMaterialCachedRestInline,
		]


class RecipeIngredientInline(admin.TabularInline):
	model = RecipeIngredient


class RecipeAdmin(admin.ModelAdmin):
	inlines = [RecipeIngredientInline]


class CalculationAdmin(admin.ModelAdmin):
	list_display = ('when_date', 'on_prescription', 'what_name', 
		'what_unit_cost', 'what_count', 'what_unit_name', 
		'what_full_cost', 'on_ingredient', 'feasible'
	)
	list_filter = ('when_date', 'on_prescription')


class ProductAdmin(admin.ModelAdmin):
	list_display  = ('name', 'is_active')
	list_editable = ('is_active',)
	list_filter   = ('is_active',)


class SaleOfferAdmin(admin.ModelAdmin):
	list_filter = ('day',)


class AccountTransactionInline(admin.TabularInline):
	model = AccountTransaction


class AccountAdmin(admin.ModelAdmin):
	inlines = [AccountTransactionInline]


admin.site.register(WorkDay,           WorkDayAdmin)
admin.site.register(FoodMaterial,      FoodMaterialAdmin)
admin.site.register(FoodMaterialItem)
admin.site.register(FoodMaterialSpend)
admin.site.register(Recipe,            RecipeAdmin)
admin.site.register(RecipeIngredient)
admin.site.register(Product,           ProductAdmin)
admin.site.register(Calculation,       CalculationAdmin)
admin.site.register(SaleOffer,         SaleOfferAdmin)
admin.site.register(Account,           AccountAdmin)
admin.site.register(AccountTransaction)
