from django.contrib import admin
from .models import (MyUser, CustomerProfile, Address,Category, Product, ProductVariant,Cart, CartItem, Order, OrderItem, Bill, BillItem)


# --------------------
# USER + PROFILE
# --------------------
@admin.register(MyUser)
class MyUserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "role", "is_active", "is_staff", "date_joined")
    list_filter = ("role", "is_active", "is_staff")
    search_fields = ("username", "email", "first_name", "last_name")


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ("customer_id", "user", "customer_name", "customer_email", "phone_number")
    search_fields = ("customer_name", "customer_email", "phone_number")
    list_filter = ("customer_email",)


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("customer", "address_line", "city", "postal_code", "country", "is_default")
    list_filter = ("country", "city", "is_default")
    search_fields = ("address_line", "city", "postal_code")


# --------------------
# PRODUCT + CATEGORY
# --------------------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "category_id")
    search_fields = ("name",)


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "is_active", "created_at")
    list_filter = ("category", "is_active")
    search_fields = ("name", "description")
    inlines = [ProductVariantInline]


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ("product", "color", "size", "stock", "price")
    list_filter = ("color", "size")
    search_fields = ("product__name",)


# --------------------
# CART
# --------------------
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("customer", "created_at", "updated_at", "total_price")
    inlines = [CartItemInline]


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("cart", "product", "variant", "quantity", "total_price")
    list_filter = ("cart", "product")
    search_fields = ("product__name", "variant__color", "variant__size")


# --------------------
# ORDER
# --------------------
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "payment_method", "payment_status", "status", "created_at")
    list_filter = ("payment_method", "payment_status", "status")
    search_fields = ("customer__customer_name", "customer__customer_email", "id")
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product", "variant", "quantity", "price", "total_price")
    search_fields = ("product__name", "variant__color", "variant__size")

class BillItemInline(admin.TabularInline):  # or StackedInline for full view
    model = BillItem
    extra = 1  # show 1 empty row for adding new items
    fields = ("product", "variant", "quantity", "price", "subtotal")
    readonly_fields = ("subtotal",)

@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "date", "total_amount", "payment_method")
    list_filter = ("payment_method", "date")
    search_fields = ("customer__customer_name", "customer__user__username")
    inlines = [BillItemInline]
