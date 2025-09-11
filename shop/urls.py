from django.urls import path
from shop.views.home import IndexView
from shop.views.customer import add_customer, customer_list, view_customer, edit_customer, deactivate_customer, activate_customer,AddAddressView,address_list,address_edit,address_delete
from shop.views.bill import (
    customer_lookup, create_bill, customer_history, billing_page,
    category_list, product_list, variant_list, register_customer  # ✅ import API views
)


urlpatterns = [
    path('', IndexView, name='Home'),
    path('add_address/',AddAddressView, name='AddAddress'),
    path('address_list/', address_list, name='address_list'),
    path('addresses/<int:pk>/edit/', address_edit, name='address_edit'),
    path('addresses/<int:pk>/delete/', address_delete, name='address_delete'),
    path('customer_lookup/', customer_lookup, name='customer_lookup'),
    path('create_bill/', create_bill, name='create_bill'),
    path('customer_history/<int:customer_id>/', customer_history, name='customer_history'),
    path('billing/', billing_page, name='billing'),
    path("register_customer/", register_customer, name="register_customer"),
    path("add_customer/",add_customer, name="add_customer"),
    path("customer_list/",customer_list, name="customer_list"),
    path("view_customer/<int:pk>/", view_customer, name="view_customer"),
    path("edit_customer/<int:pk>/", edit_customer, name="edit_customer"),
    path("deactivate_customer/<int:pk>/", deactivate_customer, name="deactivate_customer"),
    path("activate_customer/<int:pk>/", activate_customer, name="activate_customer"),

    # API URLs
    path("api/categories/", category_list, name="api_categories"),
    path("api/products/", product_list, name="api_products"),
    path("api/variants/", variant_list, name="api_variants"),
]


