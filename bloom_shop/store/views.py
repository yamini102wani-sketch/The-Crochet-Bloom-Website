from decimal import Decimal
from urllib.parse import quote
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db.models import Avg, Sum, Case, When, IntegerField
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from .forms import ContactForm, CustomOrderForm, ReviewForm, SignupForm
from .models import Category, ContactMessage, CustomOrder, Order, OrderItem, Product, Review

def _cart(request):
    return request.session.setdefault("cart", {})

def _cart_details(request):
    cart = _cart(request)
    ids = [int(k) for k in cart.keys()]
    products = Product.objects.filter(id__in=ids, active=True)
    rows, total = [], Decimal("0")
    for p in products:
        data = cart.get(str(p.id), {})
        qty = int(data.get("qty", 1))
        qty = max(1, min(qty, p.stock or 1))
        subtotal = p.price * qty
        total += subtotal
        rows.append({"product": p, "qty": qty, "size": data.get("size",""), "color": data.get("color",""), "subtotal": subtotal})
    return rows, total

def _whatsapp_url(message):
    # WhatsApp wa.me requires the international number without +, spaces or dashes.
    raw_number = str(settings.SHOP_WHATSAPP_NUMBER).strip()
    digits = "".join(ch for ch in raw_number if ch.isdigit())
    if digits.startswith("0"):
        digits = "91" + digits[1:]
    elif len(digits) == 10:
        digits = "91" + digits
    return f"https://wa.me/{digits}?text={quote(message, safe='')}"

def home(request):
    return render(request, "store/home.html", {
        "categories": Category.objects.all()[:10],
        "featured": Product.objects.filter(active=True, featured=True)[:8],
    })

def shop(request):
    products = Product.objects.filter(active=True)
    q = request.GET.get("q", "").strip()
    category = request.GET.get("category", "").strip()
    sort = request.GET.get("sort", "").strip()
    if q:
        products = products.filter(name__icontains=q) | products.filter(description__icontains=q)
    if category:
        products = products.filter(category__name=category)
    if sort == "price_low":
        products = products.order_by("price")
    elif sort == "price_high":
        products = products.order_by("-price")
    elif sort == "newest":
        products = products.order_by("-created_at")
    elif not q and not category:
        preferred = [
            "crochet-flower-bouquet", "sunflower-crochet-bag",
            "crochet-princess-doll", "crochet-teddy-bear",
            "crochet-flower-basket", "crochet-baby-booties",
            "crochet-hair-scrunchies", "crochet-coin-pouch",
        ]
        products = products.annotate(
            shop_order=Case(
                *[When(slug=slug, then=pos) for pos, slug in enumerate(preferred)],
                default=99, output_field=IntegerField()
            )
        ).order_by("shop_order", "name")
    return render(request, "store/shop.html", {"products": products, "categories": Category.objects.all(), "selected_category": category})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, active=True)
    reviews = product.reviews.filter(approved=True)
    avg = reviews.aggregate(avg=Avg("rating"))["avg"] or 0
    return render(request, "store/product_detail.html", {"product": product, "reviews": reviews, "avg_rating": round(avg, 1)})

def prices(request):
    products = Product.objects.filter(active=True).select_related("category").order_by("category__name", "name")
    return render(request, "store/prices.html", {"categories": Category.objects.all(), "products": products})

def about(request):
    return render(request, "store/about.html")

def reviews(request):
    review_list = Review.objects.filter(approved=True).select_related("product", "user")[:30]
    return render(request, "store/reviews.html", {"reviews": review_list})

def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you! Your message has been received.")
            return redirect("contact")
    else:
        form = ContactForm()
    return render(request, "store/contact.html", {"form": form})

@login_required
def custom_order(request):
    if request.method == "POST":
        form = CustomOrderForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            messages.success(request, f"Custom order {obj.custom_id} received.")
            return render(request, "store/custom_success.html", {"custom": obj, "whatsapp_url": _whatsapp_url(
                f"Hello The Crochet Bloom, I submitted custom order {obj.custom_id}. Name: {obj.customer_name}. Product type: {obj.product_type}. Please contact me for the final quote."
            )})
    else:
        form = CustomOrderForm(initial={"customer_name": request.user.get_full_name(), "email": request.user.email})
    return render(request, "store/custom_order.html", {"form": form})

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id, active=True)
    qty = max(1, int(request.POST.get("quantity", 1)))
    size = request.POST.get("size", "")
    color = request.POST.get("color", "")
    cart = _cart(request)
    cart[str(product.id)] = {"qty": min(qty, product.stock or 1), "size": size, "color": color}
    request.session.modified = True
    messages.success(request, f"{product.name} added to your cart.")
    if request.POST.get("buy_now"):
        return redirect("checkout")
    return redirect(request.META.get("HTTP_REFERER", reverse("shop")))

def cart(request):
    rows, total = _cart_details(request)
    return render(request, "store/cart.html", {"rows": rows, "total": total})

def update_cart(request):
    cart_data = _cart(request)
    for key, value in request.POST.items():
        if key.startswith("qty_"):
            pid = key.split("_", 1)[1]
            if pid in cart_data:
                try:
                    qty = max(1, int(value))
                    product = Product.objects.filter(id=int(pid)).first()
                    cart_data[pid]["qty"] = min(qty, product.stock or 1) if product else qty
                except ValueError:
                    pass
    request.session.modified = True
    return redirect("cart")

def remove_from_cart(request, product_id):
    cart_data = _cart(request)
    cart_data.pop(str(product_id), None)
    request.session.modified = True
    return redirect("cart")

@login_required
def checkout(request):
    rows, total = _cart_details(request)
    if not rows:
        messages.warning(request, "Your cart is empty.")
        return redirect("shop")
    if request.method == "POST":
        required = ["customer_name", "phone", "email", "delivery_address", "city", "pincode"]
        if any(not request.POST.get(x, "").strip() for x in required):
            messages.error(request, "Please fill all required checkout fields.")
        else:
            order = Order.objects.create(
                user=request.user,
                customer_name=request.POST["customer_name"].strip(),
                phone=request.POST["phone"].strip(),
                email=request.POST["email"].strip(),
                delivery_address=request.POST["delivery_address"].strip(),
                city=request.POST["city"].strip(),
                pincode=request.POST["pincode"].strip(),
                special_instructions=request.POST.get("special_instructions", "").strip(),
                total_amount=total,
            )
            for row in rows:
                OrderItem.objects.create(order=order, product=row["product"], quantity=row["qty"],
                                         price=row["product"].price, size=row["size"], color=row["color"])
            request.session["cart"] = {}
            request.session.modified = True
            return redirect("order_success", order_id=order.order_id)
    return render(request, "store/checkout.html", {"rows": rows, "total": total})

@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    message = _order_message(order)
    return render(request, "store/order_success.html", {"order": order, "whatsapp_url": _whatsapp_url(message)})

def _order_message(order):
    lines = [
        "Hello The Crochet Bloom,",
        "",
        "I would like to place an order.",
        f"Order ID: {order.order_id}",
        f"Customer Name: {order.customer_name}",
        f"Mobile: {order.phone}",
        f"Email: {order.email}",
        "",
        "Items:"
    ]
    for item in order.items.select_related("product"):
        lines.append(f"- {item.product.name} x {item.quantity} | Size: {item.size or 'N/A'} | Color: {item.color or 'N/A'} | ₹{item.price * item.quantity}")
    lines += [
        "",
        f"Delivery Address: {order.delivery_address}, {order.city} - {order.pincode}",
        f"Special Instructions: {order.special_instructions or 'None'}",
        f"Total Amount: ₹{order.total_amount}",
        "",
        "Thank you."
    ]
    return "\n".join(lines)

@login_required
def whatsapp_order(request, order_id):
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    return HttpResponseRedirect(_whatsapp_url(_order_message(order)))

def whatsapp_product(request, slug):
    product = get_object_or_404(Product, slug=slug, active=True)
    # Read the customer's selected options from the product page so the
    # WhatsApp message contains the actual product/order details.
    try:
        quantity = max(1, int(request.POST.get("quantity", 1)))
    except (TypeError, ValueError):
        quantity = 1
    if product.stock:
        quantity = min(quantity, product.stock)
    size = request.POST.get("size", "").strip() or "N/A"
    color = request.POST.get("color", "").strip() or "N/A"
    total = product.price * quantity
    msg = (
        "Hello The Crochet Bloom,\n\n"
        "I want to order / enquire about this product.\n"
        f"Product: {product.name}\n"
        f"Category: {product.category.name}\n"
        f"Price: ₹{product.price} each\n"
        f"Quantity: {quantity}\n"
        f"Size: {size}\n"
        f"Color: {color}\n"
        f"Estimated Total: ₹{total}\n"
        f"Description: {product.description}\n\n"
        "Please confirm availability and final price. Thank you!"
    )
    return HttpResponseRedirect(_whatsapp_url(msg))

@login_required
def dashboard(request):
    orders = request.user.orders.prefetch_related("items__product").all()
    return render(request, "store/dashboard.html", {"orders": orders})

@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id, active=True)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, "Your review was submitted for admin approval.")
    return redirect("product_detail", slug=product.slug)

def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Welcome to The Crochet Bloom!")
            return redirect("dashboard")
    else:
        form = SignupForm()
    return render(request, "registration/signup.html", {"form": form})

@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    orders = Order.objects.all()
    context = {
        "products_count": Product.objects.count(),
        "customers_count": User.objects.filter(is_staff=False).count(),
        "orders_count": orders.count(),
        "pending_count": orders.filter(status="Pending").count(),
        "completed_count": orders.filter(status="Delivered").count(),
        "revenue": orders.exclude(status="Cancelled").aggregate(total=Sum("total_amount"))["total"] or Decimal("0"),
        "enquiries_count": ContactMessage.objects.filter(status="New").count(),
        "reviews_count": Review.objects.filter(approved=False).count(),
        "recent_orders": orders[:8],
    }
    return render(request, "store/admin_dashboard.html", context)
