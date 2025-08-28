from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from shop.models import CustomerProfile, Bill, BillItem, Product, ProductVariant

def billing_page(request):
    return render(request, "bill.html")

def customer_lookup(request):
    phone = request.GET.get("phone")
    if not phone:
        return JsonResponse({"error": "Phone number required"}, status=400)

    try:
        customer = CustomerProfile.objects.get(phone_number=phone)
        return JsonResponse({
            "exists": True,
            "name": customer.customer_name,
            "email": customer.customer_email,
            "id": customer.id
        })
    except CustomerProfile.DoesNotExist:
        return JsonResponse({"exists": False})


from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
import json

@csrf_exempt
@transaction.atomic
def create_bill(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    customer_id = data.get("customer_id")
    if not customer_id:
        return JsonResponse({"error": "Customer ID required"}, status=400)

    customer = get_object_or_404(CustomerProfile, id=customer_id)

    items = data.get("items", [])
    if not items:
        return JsonResponse({"error": "No items provided"}, status=400)

    bill = Bill.objects.create(customer=customer, total_amount=0, payment_method=data.get("payment_method", "cash"))

    total = 0
    for item in items:
        product = get_object_or_404(Product, id=item.get("product_id"))
        variant = None
        if item.get("variant_id"):
            variant = get_object_or_404(ProductVariant, id=item["variant_id"])
            if variant.stock < int(item["quantity"]):
                return JsonResponse({"error": f"Insufficient stock for {variant}"}, status=400)

        qty = int(item["quantity"])
        price = float(item["price"])
        subtotal = qty * price

        BillItem.objects.create(bill=bill, product=product, variant=variant, quantity=qty, price=price)

        total += subtotal
        if variant:
            variant.stock -= qty
            variant.save()

    discount = float(data.get("discount", 0))
    bill.total_amount = max(total - discount, 0)
    bill.save()

    return JsonResponse({
        "bill_id": bill.id,
        "customer": bill.customer.customer_name,
        "total_amount": bill.total_amount,
        "items": bill.items.count()
    })


def customer_history(request, customer_id):
    customer = get_object_or_404(CustomerProfile, id=customer_id)
    bills = customer.bills.all().order_by("-date")

    history = []
    total_spent = 0
    for bill in bills:
        items = [
            {
                "product": item.product.name,
                "variant": f"{item.variant.color}, {item.variant.size}" if item.variant else None,
                "quantity": item.quantity,
                "price": float(item.price),
                "subtotal": float(item.subtotal)
            }
            for item in bill.items.all()
        ]
        total_spent += float(bill.total_amount)

        history.append({
            "bill_id": bill.id,
            "date": bill.date.strftime("%Y-%m-%d %H:%M"),
            "total": float(bill.total_amount),
            "items": items
        })

    return JsonResponse({
        "customer": customer.customer_name,
        "phone": customer.phone_number,
        "total_spent": total_spent,
        "total_visits": bills.count(),
        "bills": history
    })

# API: Get all categories
def category_list(request):
    from shop.models import Category
    categories = Category.objects.all().values("id", "name")
    return JsonResponse(list(categories), safe=False)

# API: Get products filtered by category
def product_list(request):
    from shop.models import Product
    category_id = request.GET.get("category")
    products = Product.objects.filter(category_id=category_id).values("id", "name")
    return JsonResponse(list(products), safe=False)

# API: Get variants filtered by product
def variant_list(request):
    from shop.models import ProductVariant
    product_id = request.GET.get("product")
    variants = ProductVariant.objects.filter(product_id=product_id).values("id", "color", "size", "price")
    return JsonResponse(list(variants), safe=False)
