from django.conf.urls import include, url

from . import views


urlpatterns = [
	url(r'^$',                      views.index,                          name='main_menu'),
	url(r'^login$',                 views.login_view,                     name='login'),
	url(r'^food_material_import$',  views.food_material_import,           name='food_material_import'),
	url(r'^food_material_list$',    views.FoodMaterialListView.as_view(), name='food_material_list'),
	url(r'^product_list$',          views.ProductListView.as_view(),      name='product_list'),
	url(r'^simple_product_import$', views.simple_product_import,          name='simple_product_import'),
]
