# The Crochet Bloom — Crochet Products Ordering System

A professional full-stack Django e-commerce/order-management website for a handmade crochet business.

## Technology
- Python 3
- Django 5
- HTML5
- CSS3
- JavaScript
- Bootstrap 5
- SQLite
- Django ORM
- Django Authentication
- WhatsApp pre-filled order links

## Features
- Premium responsive crochet-themed UI
- Home page with hero carousel and categories
- Database-driven shop and product details
- Search, category filter and sorting
- Session-based shopping cart
- Checkout and automatic Order ID
- WhatsApp pre-filled order message
- Customer signup/login/dashboard/order history
- Custom crochet order with image upload
- Customer reviews with admin approval
- Contact/enquiry form
- Django admin product/category/order/customer/review/enquiry management
- Custom admin dashboard with statistics
- Order status workflow: Pending, Confirmed, Preparing, Ready, Shipped, Delivered, Cancelled

## Windows setup

Open Command Prompt or PowerShell inside this folder.

```bat
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py seed_demo
python manage.py createsuperuser
python manage.py runserver
```

Open:
- Website: http://127.0.0.1:8000/
- Django Admin: http://127.0.0.1:8000/admin/
- Custom Admin Dashboard: http://127.0.0.1:8000/admin-dashboard/

## Demo data
After migration, run `python manage.py seed_demo` to add 10 crochet categories and 10 sample products. Add your own product photos from Django Admin.

## WhatsApp number
Open `crochet_site/settings.py` and change:

```python
SHOP_WHATSAPP_NUMBER = "917760787770"
```

Use digits only with country code. Example for India: `91XXXXXXXXXX`.

The website uses a WhatsApp `wa.me` link with a pre-filled message. The customer must press **Send** inside WhatsApp.

## Adding products
1. Create/login to the Django admin.
2. Add Categories.
3. Add Products with name, slug, description, price, image, colors, sizes and stock.
4. Mark selected products as Featured.
5. Add approved reviews if desired.

## Notes
- SQLite is intended for college/demo/development use.
- For production deployment, use environment variables for secrets and WhatsApp/business settings, a production database, HTTPS, secure cookies and a proper media storage service.
- The included SVG images are local placeholders so the project can run immediately. Replace them with your own crochet product photographs from Admin for a real shop.

## First run (Windows)
1. Open the terminal inside the folder that contains `manage.py`.
2. Activate the virtual environment: `venv\Scripts\activate`
3. Install packages: `pip install -r requirements.txt`
4. Apply database migrations: `python manage.py migrate`
5. Create demo categories/products: `python manage.py seed_demo`
6. (Optional) Create admin login: `python manage.py createsuperuser`
7. Start the website: `python manage.py runserver`

The Shop page includes a **Buy Now** button on every product card. It adds that product to the cart and opens checkout.


Product images are bundled in media/products and seed_demo assigns them to demo products.
