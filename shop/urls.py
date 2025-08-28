from django.urls import path
from shop.views.home import IndexView, AddressView, AddAddressView
from shop.views.bill import (
    customer_lookup, create_bill, customer_history, billing_page,
    category_list, product_list, variant_list  # ✅ import API views
)

urlpatterns = [
    path('', IndexView, name='Home'),
    path('Address', AddressView, name='Address'),
    path('add_address', AddAddressView, name='AddAddress'),
    path('customer_lookup', customer_lookup, name='customer_lookup'),
    path('create_bill', create_bill, name='create_bill'),
    path('customer_history/<int:customer_id>', customer_history, name='customer_history'),
    path('billing', billing_page, name='billing'),

    # API URLs
    path("api/categories/", category_list, name="api_categories"),
    path("api/products/", product_list, name="api_products"),
    path("api/variants/", variant_list, name="api_variants"),
]
