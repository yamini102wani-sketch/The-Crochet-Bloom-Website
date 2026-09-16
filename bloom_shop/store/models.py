from decimal import Decimal
import uuid
from django.contrib.auth.models import User
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="categories/", blank=True, null=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="products")
    name = models.CharField(max_length=180)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    colors = models.CharField(max_length=300, blank=True, help_text="Comma separated")
    sizes = models.CharField(max_length=200, blank=True, help_text="Comma separated")
    stock = models.PositiveIntegerField(default=10)
    featured = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-featured", "-created_at"]

    def __str__(self):
        return self.name

    def color_list(self):
        return [x.strip() for x in self.colors.split(",") if x.strip()]

    def size_list(self):
        return [x.strip() for x in self.sizes.split(",") if x.strip()]

class Order(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"), ("Confirmed", "Confirmed"), ("Preparing", "Preparing"),
        ("Ready", "Ready"), ("Shipped", "Shipped"), ("Delivered", "Delivered"),
        ("Cancelled", "Cancelled"),
    ]
    PAYMENT_CHOICES = [("Pending", "Pending"), ("Paid", "Paid"), ("COD", "COD")]
    order_id = models.CharField(max_length=20, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="orders")
    customer_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    delivery_address = models.TextField()
    city = models.CharField(max_length=80)
    pincode = models.CharField(max_length=10)
    special_instructions = models.TextField(blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    payment_status = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = "CB" + uuid.uuid4().hex[:8].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_id

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    size = models.CharField(max_length=80, blank=True)
    color = models.CharField(max_length=80, blank=True)

    def line_total(self):
        return self.price * self.quantity

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveSmallIntegerField(default=5)
    text = models.TextField()
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

class ContactMessage(models.Model):
    STATUS_CHOICES = [("New", "New"), ("Read", "Read"), ("Resolved", "Resolved")]
    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=180)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="New")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} - {self.name}"

class CustomOrder(models.Model):
    STATUS_CHOICES = [("New", "New"), ("Contacted", "Contacted"), ("Confirmed", "Confirmed"), ("Completed", "Completed")]
    custom_id = models.CharField(max_length=20, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    customer_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    product_type = models.CharField(max_length=150)
    preferred_color = models.CharField(max_length=100, blank=True)
    preferred_size = models.CharField(max_length=100, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    design_description = models.TextField()
    special_instructions = models.TextField(blank=True)
    reference_image = models.ImageField(upload_to="custom_orders/", blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="New")
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.custom_id:
            self.custom_id = "CO" + uuid.uuid4().hex[:8].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.custom_id
