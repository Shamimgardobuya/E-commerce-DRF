from django.core.management.base import BaseCommand
from categories.models import Category


class Command(BaseCommand):
    help = "Seeder for creating custom categories and products"

    def handle(self, *args, **options):
        parent_categories = [
            "Pastries",
            "Beverages",
            "Fruits & Vegetables",
        ]
        child_categories = {
            "Pastries": ["cakes", "bread", "cookies"],
            "Beverages": ["soft drinks", "smoothies"],
            "Fruits & Vegetables": ["mangoes", "apples", "tomatoes"],
        }
        for parent_category in parent_categories:

            parent_exists, new_parent_category = Category.objects.get_or_create(
                category_name=parent_category
            )

        new_categories = [
            Category(
                category_name=child,
                parent=Category.objects.filter(category_name=parent_categ).get(),
            )
            for parent_categ, child_categ in child_categories.items()
            for child in child_categ
        ]
        if len(new_categories) > 0:
            try:
                Category.objects.bulk_create(new_categories)
                self.stdout.write(
                    self.style.SUCCESS("Created child categories successfully: ")
                )
                

            except Exception as e:
                self.stdout.write(
                    self.style.WARNING(
                        f"Error has occurred '{e}' not found — skipping."
                    )
                )
