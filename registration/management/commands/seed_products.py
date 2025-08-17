from django.core.management.base import BaseCommand
from products.models import Product
from categories.models import Category


class Command(BaseCommand):
    help = "Seeder for creating products"

    def handle(self, *args, **options):
        products = [
            {"name": "Strawberry cake", "quantity": 5, "price": 340.00, "weight": 400, "category": {"Pastries": "cakes"}  },
            {"name": "Chocolate cookies", "quantity": 17, "price": 240.00, "weight": 300 , "category": {"Pastries": "cookies"}   }

        ]
        
        created_products = []
        for prod in products:
                # Get parent and child category names
                parent_name, child_name = list(prod["category"].items())[0]

                # Ensure parent exists
                parent_cat, _ = Category.objects.get_or_create(category_name=parent_name, parent=None)

                # Ensure child exists (linked to parent)
                child_cat, _ = Category.objects.get_or_create(category_name=child_name, parent=parent_cat)

                # Create product
                product = Product(
                    name=prod["name"],
                    quantity=prod["quantity"],
                    price=prod["price"],
                    weight=prod["weight"],
                    category=child_cat
                )
                created_products.append(product)

        try:
                Product.objects.bulk_create(created_products, ignore_conflicts=True)
                self.stdout.write(self.style.SUCCESS(f"Created {len(created_products)} products successfully."))
        except Exception as e:
                self.stdout.write(
                    self.style.WARNING(f"Error has occurred '{e}' not found — skipping.")
                )
