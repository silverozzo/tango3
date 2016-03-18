from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators        import login_required
from django.http                           import HttpResponse
from django.shortcuts                      import render, redirect, get_object_or_404
from django.utils.decorators               import method_decorator
from django.views                          import generic

from .models   import FoodMaterial, Product, SaleOffer, WorkDay, Account, AccountTransaction
from .services import FoodMaterialImportService, SimpleProductImportService, ComplexProductImportService


def index(request):
	return render(request, 'bar/main_menu.html', {})


@staff_member_required
def food_material_import(request):
	if request.FILES and request.FILES['import']:
		FoodMaterialImportService.run(request.FILES['import'])
	return redirect('bar:food_material_list')


@staff_member_required
def simple_product_import(request):
	if request.FILES and request.FILES['import']:
		SimpleProductImportService.run(request.FILES['import'], request.POST['prefix'])
	return redirect('bar:product_list')


@staff_member_required
def complex_product_import(request):
	if request.FILES and request.FILES['import']:
		ComplexProductImportService.run(request.FILES['import'], request.POST['prefix'])
	return redirect('bar:product_list')


@staff_member_required
def sale_offer_generator(request):
	SaleOffer.generate()
	return redirect('bar:sale_offer_list')


@staff_member_required
def add_transaction_form(request):
	if request.POST['sale_offer'] and request.POST['account']:
		transaction = AccountTransaction(
			account    = get_object_or_404(Account,   pk=request.POST['account']),
			sale_offer = get_object_or_404(SaleOffer, pk=request.POST['sale_offer']),
			day        = WorkDay.get_current()
		)
		transaction.save()
	return redirect('bar:transaction_list')


@staff_member_required
def add_account_form(request):
	if request.POST['name']:
		account = Account(
			name       = request.POST['name'],
			is_default = request.POST.get('is_default', False),
			costed     = request.POST.get('costed',     False),
		)
		account.save()
	return redirect('bar:transaction_list')


class FoodMaterialListView(generic.ListView):
	model               = FoodMaterial
	template_name       = 'bar/food_material_list.html'
	context_object_name = 'food_materials'
	
	def get_context_data(self, **kwargs):
		context = super(FoodMaterialListView, self).get_context_data(**kwargs)
		context['user']  = self.request.user
		return context


class ProductListView(generic.ListView):
	model               = Product
	template_name       = 'bar/product_list.html'
	context_object_name = 'products'
	
	def get_queryset(self):
		return Product.objects.order_by('name')
	
	def get_context_data(self, **kwargs):
		context = super(ProductListView, self).get_context_data(**kwargs)
		context['user']  = self.request.user
		return context


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


class TransactionListView(generic.ListView):
	model               = AccountTransaction
	template_name       = 'bar/transaction_list.html'
	context_object_name = 'transactions'
	
	@method_decorator(login_required(login_url='/admin/login/'))
	def dispatch(self, request, *args, **kwargs):
		return super(TransactionListView, self).dispatch(request, *args, **kwargs)
	
	def get_queryset(self):
		day = WorkDay.get_current()
		return AccountTransaction.objects.filter(day=day)
	
	def get_context_data(self, **kwargs):
		day = WorkDay.get_current()
		
		context = super(TransactionListView, self).get_context_data(**kwargs)
		context['user']     = self.request.user
		context['today']    = day
		context['offers']   = SaleOffer.objects.filter(day=day, feasible=True)
		context['accounts'] = Account.objects.all()
		context['totals']   = AccountTransaction.get_totals(day)
		return context
