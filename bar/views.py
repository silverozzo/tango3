from django.http      import HttpResponse
from django.shortcuts import render
from django.views     import generic

from .models   import FoodMaterial, Product
from .services import FoodMaterialImportService, SimpleProductImportService


def index(request):
	if request.user.is_authenticated():
		return render(request, 'bar/main_menu.html', {})
	else:
		return redirect('bar:login')


def login_view(request):
	pass


def food_material_import(request):
	if request.FILES and request.FILES['import']:
		FoodMaterialImportService.run(request.FILES['import'])
		return HttpResponse('file is here!')
	else:
		return HttpResponse('file lost..')


def simple_product_import(request):
	if request.FILES and request.FILES['import']:
		SimpleProductImportService.run(request.FILES['import'])
		return HttpResponse('file is here!')
	else:
		return HttpResponse('file lost..')


class FoodMaterialListView(generic.ListView):
	model               = FoodMaterial
	template_name       = 'bar/food_material_list.html'
	context_object_name = 'food_materials'


class ProductListView(generic.ListView):
	model               = Product
	template_name       = 'bar/product_list.html'
	context_object_name = 'products'
