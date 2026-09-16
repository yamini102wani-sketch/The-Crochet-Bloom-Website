from django.core.management.base import BaseCommand
from django.conf import settings
from store.models import Category, Product



class Command(BaseCommand):
    help = "Populate The Crochet Bloom with demo categories and products."

    def handle(self, *args, **options):
        data = {
            "Flower Bouquets": "Long-lasting handmade crochet flower arrangements.",
            "Crochet Bags": "Stylish handmade bags for everyday use.",
            "Crochet Dolls": "Adorable handmade dolls with customizable colors and details.",
            "Cute Toys": "Soft, playful crochet toys for gifting and collecting.",
            "Home Decor": "Cozy crochet accents for your home.",
            "Baby Essentials": "Soft and comfortable crochet essentials for little ones.",
            "Hair Accessories": "Cute crochet flowers, clips and scrunchies.",
            "Cute Pouches": "Small practical pouches for everyday essentials.",
            "Amigurumi Keychains": "Tiny handmade keychains that make lovely gifts.",
            "Cozy Wearables": "Warm and comfortable crochet hats, scarves and wearables.",
            "Seasonal & Festive Decor": "Handmade decorations for festivals and celebrations.",
        }
        cats = {}
        for name, desc in data.items():
            cats[name], _ = Category.objects.get_or_create(
                name=name, defaults={"description": desc}
            )

        products = [
            ("Crochet Flower Bouquet", "Flower Bouquets", 499, "A long-lasting handmade flower bouquet.", "Pink,Lilac,Peach,White", "Small,Medium,Large"),
            ("Sunflower Crochet Bag", "Crochet Bags", 699, "Beautiful crochet bag with floral detail.", "Cream,Yellow,Beige", "Medium"),
            ("Crochet Princess Doll", "Crochet Dolls", 799, "Charming handmade doll with customizable outfit.", "Pink,Lilac,Peach", "Medium,Large"),
            ("Crochet Teddy Bear", "Cute Toys", 599, "Soft handmade teddy bear for gifting.", "Pink,Brown,Cream", "Small,Medium,Large"),
            ("Crochet Flower Basket", "Home Decor", 549, "Adds a touch of warmth to your space.", "White,Yellow,Green", "Medium,Large"),
            ("Crochet Baby Booties", "Baby Essentials", 399, "Soft and cozy crochet footwear for little feet.", "Pink,White,Cream", "0-3M,3-6M,6-12M"),
            ("Crochet Hair Scrunchies", "Hair Accessories", 299, "Stylish and comfortable crochet hair accessories.", "Pink,Lilac,Yellow", "One Size"),
            ("Crochet Coin Pouch", "Cute Pouches", 349, "Small, cute and useful pouch for coins and more.", "Green,Pink,Cream", "Small,Medium"),
            ("Crochet Bunny Keychain", "Amigurumi Keychains", 199, "Cute handmade bunny keychain.", "Pink,White,Beige", "Small"),
            ("Cozy Crochet Hat", "Cozy Wearables", 449, "Soft everyday crochet hat.", "Cream,Brown,Pink", "S,M,L"),
            ("Festive Christmas Tree", "Seasonal & Festive Decor", 499, "Handmade Christmas crochet decoration.", "Green,Red,Cream", "Medium,Large"),
        ]

        featured_names = {
            "Crochet Flower Bouquet", "Sunflower Crochet Bag", "Crochet Princess Doll",
            "Crochet Teddy Bear", "Crochet Flower Basket", "Crochet Baby Booties",
            "Crochet Hair Scrunchies", "Crochet Coin Pouch"
        }

        image_map = {
            "Crochet Flower Bouquet": "products/flower_bouquet.jpg",
            "Sunflower Crochet Bag": "products/sunflower_bag.jpg",
            "Crochet Princess Doll": "products/princess_doll.jpg",
            "Crochet Teddy Bear": "products/teddy_bear.jpg",
            "Crochet Flower Basket": "products/flower_basket.jpg",
            "Crochet Baby Booties": "products/baby_booties.jpg",
            "Crochet Hair Scrunchies": "products/hair_scrunchies.jpg",
            "Crochet Coin Pouch": "products/coin_pouch.jpg",
            "Crochet Bunny Keychain": "products/crochet_bunny_keychain.jpg",
            "Cozy Crochet Hat": "products/cozy_crochet_hat.jpg",
            "Festive Christmas Tree": "products/festive_christmas_tree.jpg",
        }

        for name, cat, price, desc, colors, sizes in products:
            slug = name.lower().replace(" ", "-")
            Product.objects.update_or_create(
                slug=slug,
                defaults={
                    "category": cats[cat],
                    "name": name,
                    "description": desc,
                    "price": price,
                    "image": image_map.get(name, ""),
                    "colors": colors,
                    "sizes": sizes,
                    "stock": 20,
                    "featured": name in featured_names,
                    "active": True,
                },
            )

        self.stdout.write(self.style.SUCCESS("Demo categories and products added successfully."))
