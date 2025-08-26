from django.shortcuts import render



def IndexView(request):
    return render(request, 'index.html')

def AddressView(request):
    return render(request, 'Address.html')

def AddAddressView(request):
    return render(request, 'add_address.html')



