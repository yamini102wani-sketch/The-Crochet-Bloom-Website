# Generated manually for the Crochet Products Ordering System.
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120, unique=True)),
                ("description", models.TextField(blank=True)),
                ("image", models.ImageField(blank=True, null=True, upload_to="categories/")),
            ],
            options={"verbose_name_plural": "Categories", "ordering": ["name"]},
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=180)),
                ("slug", models.SlugField(unique=True)),
                ("description", models.TextField()),
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("image", models.ImageField(blank=True, null=True, upload_to="products/")),
                ("colors", models.CharField(blank=True, help_text="Comma separated", max_length=300)),
                ("sizes", models.CharField(blank=True, help_text="Comma separated", max_length=200)),
                ("stock", models.PositiveIntegerField(default=10)),
                ("featured", models.BooleanField(default=False)),
                ("active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("category", models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="products", to="store.category")),
            ],
            options={"ordering": ["-featured", "-created_at"]},
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("order_id", models.CharField(editable=False, max_length=20, unique=True)),
                ("customer_name", models.CharField(max_length=150)),
                ("phone", models.CharField(max_length=20)),
                ("email", models.EmailField(max_length=254)),
                ("delivery_address", models.TextField()),
                ("city", models.CharField(max_length=80)),
                ("pincode", models.CharField(max_length=10)),
                ("special_instructions", models.TextField(blank=True)),
                ("total_amount", models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ("status", models.CharField(choices=[("Pending", "Pending"), ("Confirmed", "Confirmed"), ("Preparing", "Preparing"), ("Ready", "Ready"), ("Shipped", "Shipped"), ("Delivered", "Delivered"), ("Cancelled", "Cancelled")], default="Pending", max_length=20)),
                ("payment_status", models.CharField(choices=[("Pending", "Pending"), ("Paid", "Paid"), ("COD", "COD")], default="Pending", max_length=20)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("user", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="orders", to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="ContactMessage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120)),
                ("email", models.EmailField(max_length=254)),
                ("phone", models.CharField(blank=True, max_length=20)),
                ("subject", models.CharField(max_length=180)),
                ("message", models.TextField()),
                ("status", models.CharField(choices=[("New", "New"), ("Read", "Read"), ("Resolved", "Resolved")], default="New", max_length=20)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="CustomOrder",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("custom_id", models.CharField(editable=False, max_length=20, unique=True)),
                ("customer_name", models.CharField(max_length=150)),
                ("phone", models.CharField(max_length=20)),
                ("email", models.EmailField(max_length=254)),
                ("product_type", models.CharField(max_length=150)),
                ("preferred_color", models.CharField(blank=True, max_length=100)),
                ("preferred_size", models.CharField(blank=True, max_length=100)),
                ("quantity", models.PositiveIntegerField(default=1)),
                ("design_description", models.TextField()),
                ("special_instructions", models.TextField(blank=True)),
                ("reference_image", models.ImageField(blank=True, null=True, upload_to="custom_orders/")),
                ("status", models.CharField(choices=[("New", "New"), ("Contacted", "Contacted"), ("Confirmed", "Confirmed"), ("Completed", "Completed")], default="New", max_length=20)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("user", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="OrderItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("quantity", models.PositiveIntegerField(default=1)),
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("size", models.CharField(blank=True, max_length=80)),
                ("color", models.CharField(blank=True, max_length=80)),
                ("order", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="items", to="store.order")),
                ("product", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="store.product")),
            ],
        ),
        migrations.CreateModel(
            name="Review",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("rating", models.PositiveSmallIntegerField(default=5)),
                ("text", models.TextField()),
                ("approved", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("product", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="reviews", to="store.product")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="reviews", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-created_at"]},
        ),
    ]
