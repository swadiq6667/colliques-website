from django.urls import path
from shop.views.home import IndexView, AddressView, AddAddressView # import your view file # import your view file

urlpatterns = [
    path('', IndexView, name='Home'),
    path('Address', AddressView, name='Address'),
    path('add_address', AddAddressView, name='AddAddress'),
    
    




]