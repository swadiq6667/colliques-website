from django.shortcuts import render, redirect,get_object_or_404
from django.http import JsonResponse
from shop.models import CustomerProfile, Address, MyUser
from shop.forms import CustomerRegisterForm, CustomerForm, AddressForm
from django.contrib import messages
from django.db.models import Q



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
    customer_id = request.GET.get("customer")  # optional pre-filter
    addresses = Address.objects.all()
    if customer_id:
        addresses = addresses.filter(customer_id=customer_id)

    customers = CustomerProfile.objects.all()

    if request.method == "POST":
        # 1. Get the selected customer instance
        customer_pk = request.POST.get("customer")
        customer = get_object_or_404(CustomerProfile, pk=customer_pk)

        # 2. Create and save the Address object
        Address.objects.create(
            customer=customer,
            address_line=request.POST.get("address_line"),
            city=request.POST.get("city"),
            postal_code=request.POST.get("postal_code"),
            country=request.POST.get("country"),
            address_type=request.POST.get("address_type"),
            is_default=bool(request.POST.get("is_default")),
        )

        messages.success(request, "Address saved successfully.")
        return redirect("address_list")  # or wherever you list addresses

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
    query = request.GET.get("q", "").strip()      # read ?q=...
    addresses = Address.objects.select_related('customer').all()

    if query:                                     # apply filter if search text entered
        addresses = addresses.filter(
            Q(customer__customer_name__icontains=query) |
            Q(customer__phone_number__icontains=query) |
            Q(address_line__icontains=query) |
            Q(city__icontains=query) |
            Q(postal_code__icontains=query)
        )

    return render(
        request,
        "Address.html",
        {
            "addresses": addresses,
            "query": query,                       # so template can keep the value in the input
        },
    )   

def address_edit(request, pk):
    address = get_object_or_404(Address, pk=pk)

    if request.method == "POST":
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            messages.success(request, "Address updated successfully.")
            return redirect("address_list")        # redirect after successful update
    else:
        form = AddressForm(instance=address)

    # ALWAYS return a response for GET or invalid POST
    return render(request, "add_address.html", {
        "form": form,
        "address": address,      # so your template can show existing values
        "customers": [address.customer],  # if your template needs this dropdown
    })
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
    customer = get_object_or_404(CustomerProfile, pk=pk)
    user = customer.user  # assuming CustomerProfile has a OneToOne to MyUser

    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            # Update MyUser fields
            user.username  = form.cleaned_data['username']
            user.email     = form.cleaned_data['email']
            if form.cleaned_data['password']:
                user.set_password(form.cleaned_data['password'])
            user.first_name = form.cleaned_data['first_name']
            user.last_name  = form.cleaned_data['last_name']
            user.save()

            # Update CustomerProfile fields
            customer.phone_number = form.cleaned_data['phone_number']
            customer.save()

            return redirect("customer_list")   # <-- must return HttpResponse
    else:
        # Pre-populate the form
        form = CustomerForm(initial={
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'phone_number': customer.phone_number,
        })

    return render(request, "edit_customer.html", {"form": form, "customer": customer})  

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