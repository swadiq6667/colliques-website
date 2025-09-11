from django.shortcuts import render, redirect
from django.http import JsonResponse
from shop.models import CustomerProfile, Address, MyUser
from shop.forms import CustomerRegisterForm, CustomerForm, AddressForm
from django.contrib import messages


def add_customer(request):
    if request.method == "POST":
        customer_form = CustomerForm(request.POST)
        address_form = AddressForm(request.POST)

        if customer_form.is_valid():
            # Extract form data
            username = customer_form.cleaned_data['username']
            email = customer_form.cleaned_data['email']
            password = customer_form.cleaned_data['password']
            first_name = customer_form.cleaned_data['first_name']
            last_name = customer_form.cleaned_data['last_name']
            phone_number = customer_form.cleaned_data['phone_number']

            # Auto-generate customer_name
            customer_name = f"{first_name} {last_name}".strip()

            # 1️⃣ Create or update User
            user, created = MyUser.objects.get_or_create(
                username=username,
                defaults={
                    "email": email,
                    "first_name": first_name,
                    "last_name": last_name,
                    "role": "Customer"
                }
            )
            if created:
                user.set_password(password)
            else:
                # Update existing user info
                user.email = email
                user.first_name = first_name
                user.last_name = last_name
            user.save()

            # 2️⃣ Create or update CustomerProfile
            customer, created = CustomerProfile.objects.get_or_create(
                user=user,
                defaults={
                    "customer_name": customer_name,
                    "customer_email": email,
                    "phone_number": phone_number
                }
            )
            if not created:
                customer.customer_name = customer_name
                customer.customer_email = email
                customer.phone_number = phone_number
                customer.save()

            # 3️⃣ Save Address (if any)
            if address_form.is_valid() and any(address_form.cleaned_data.values()):
                address = address_form.save(commit=False)
                address.customer = customer
                address.save()

            messages.success(request, "✅ Customer added successfully!")
            return redirect("add_customer")

        else:
            messages.error(request, "❌ Please correct errors in customer form")

    else:
        customer_form = CustomerForm()
        address_form = AddressForm()

    return render(request, "add_customer.html", {
        "customer_form": customer_form,
        "address_form": address_form,
    })

def AddAddressView(request):
    # Get ?customer=<id> from the query string if present
    customer_id = request.GET.get("customer")

    # Start with all addresses
    addresses = Address.objects.all()

    # If a specific customer id is passed, filter to only their addresses
    if customer_id:
        addresses = addresses.filter(customer_id=customer_id)

    # Send all customers so you can build a dropdown
    customers = CustomerProfile.objects.all()

    return render(
        request,
        "add_address.html",
        {
            "addresses": addresses,
            "customers": customers,
            "selected_customer": customer_id,
        },
    )

def address_list(request):
    addresses = Address.objects.select_related('customer').all()
    return render(request, 'Address.html', {'addresses': addresses})

def address_edit(request, pk):
    address = get_object_or_404(Address, pk=pk)
    # reuse your form template to edit
    # handle POST/GET logic here
    ...

def address_delete(request, pk):
    address = get_object_or_404(Address, pk=pk)
    address.delete()
    return redirect('address_list')

def customer_list(request):
    customers = CustomerProfile.objects.select_related("user").all()
    return render(request, "customer_list.html", {"customers": customers})

def view_customer(request, pk):
    customer = get_object_or_404(CustomerProfile, pk=pk)
    return render(request, "view_customer.html", {"customer": customer})

def edit_customer(request, pk):
    # You can reuse CustomerForm here
    pass  

def deactivate_customer(request, pk):
    customer = get_object_or_404(CustomerProfile, pk=pk)
    customer.user.is_active = False
    customer.user.save()
    return redirect("customer_list")

def activate_customer(request, pk):
    customer = get_object_or_404(CustomerProfile, pk=pk)
    customer.user.is_active = True
    customer.user.save()
    return redirect("customer_list")