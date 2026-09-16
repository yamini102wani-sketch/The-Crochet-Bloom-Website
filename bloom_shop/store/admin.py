from django.contrib import admin
from .models import Category, Product, Order, OrderItem, Review, ContactMessage, CustomOrder

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "stock", "featured", "active", "created_at")
    list_filter = ("category", "featured", "active")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("price",)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("order_id", "customer_name", "phone", "total_amount", "status", "payment_status", "created_at")
    list_filter = ("status", "payment_status", "created_at")
    search_fields = ("order_id", "customer_name", "phone", "email")
    inlines = [OrderItemInline]

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("product", "user", "rating", "approved", "created_at")
    list_filter = ("approved", "rating")
    search_fields = ("text", "user__username", "product__name")

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("subject", "name", "email", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("subject", "name", "email", "message")

@admin.register(CustomOrder)
class CustomOrderAdmin(admin.ModelAdmin):
    list_display = ("custom_id", "customer_name", "product_type", "quantity", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("custom_id", "customer_name", "phone", "product_type")

admin.site.site_header = "The Crochet Bloom — Admin"
admin.site.site_title = "The Crochet Bloom"
admin.site.index_title = "Crochet Products Ordering System"
