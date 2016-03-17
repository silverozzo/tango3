from django.http      import HttpResponse
from django.shortcuts import render, redirect
from django.views     import generic

from .models   import FoodMaterial, Product, SaleOffer, WorkDay
from .services import FoodMaterialImportService, SimpleProductImportService, ComplexProductImportService


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
		SimpleProductImportService.run(request.FILES['import'], request.POST['prefix'])
		return HttpResponse('file is here!')
	else:
		return HttpResponse('file lost..')


def complex_product_import(request):
	if request.FILES and request.FILES['import']:
		ComplexProductImportService.run(request.FILES['import'], request.POST['prefix'])
		return HttpResponse('file is here!')
	else:
		return HttpResponse('file lost...')


def sale_offer_generator(request):
	SaleOffer.generate()
	return redirect('bar:sale_offer_list')


class FoodMaterialListView(generic.ListView):
	model               = FoodMaterial
	template_name       = 'bar/food_material_list.html'
	context_object_name = 'food_materials'


class ProductListView(generic.ListView):
	model               = Product
	template_name       = 'bar/product_list.html'
	context_object_name = 'products'


class SaleOfferListView(generic.ListView):
	model               = SaleOffer
	template_name       = 'bar/sale_offer_list.html'
	context_object_name = 'sale_offers'
	
	def get_queryset(self):
		day = WorkDay.get_current()
		return SaleOffer.objects.filter(day=day)
	
	def get_context_data(self, **kwargs):
		context = super(SaleOfferListView, self).get_context_data(**kwargs)
		context['user']  = self.request.user
		context['today'] = WorkDay.get_current()
		return context
