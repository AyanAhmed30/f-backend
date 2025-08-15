from django.core.management.base import BaseCommand
from printbookcalculator.models import *

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        # --- Trim Sizes (from your calculation table) ---
        trim_sizes = {
            "Pocket Book (4.25 x 6.87 in)": {},
            "Digest (5.5 x 8.5 in)": {},
            "US Trade (6 x 9 in)": {},
            "Royal (6.14 x 9.21 in)": {},
            "US Letter (8.5 x 11 in)": {},
            "Square (8.5 x 8.5 in)": {},
            "A4": {},
            "A5": {},
            "Executive (7 x 10 in)": {},
            "Crown Quarto (7.44 x 9.68 in)": {},
            "Novella (5 x 8 in)": {},
        }
        # Create and store TrimSize objects
        for trim_name in trim_sizes:
            trim_sizes[trim_name]['obj'] = TrimSize.objects.get_or_create(name=trim_name)[0]

        # --- Interior Colors ---
        InteriorColor.objects.get_or_create(name="Standard Black & White", price_per_page=0.01)
        InteriorColor.objects.get_or_create(name="Premium Black & White", price_per_page=0.02)
        InteriorColor.objects.get_or_create(name="Standard Color", price_per_page=0.03)
        InteriorColor.objects.get_or_create(name="Premium Color", price_per_page=0.10)

        # --- Paper Types ---
        PaperType.objects.get_or_create(name="60# Cream-Uncoated", price_per_page=0.01)
        PaperType.objects.get_or_create(name="80# White-Coated", price_per_page=0.02)

        # --- Cover Finishes ---
        CoverFinish.objects.get_or_create(name="Gloss", price=0.20)
        CoverFinish.objects.get_or_create(name="Matte", price=0.20)

        # --- Binding Types for each Trim Size ---
        # Format: (Binding Name, Price, min_pages, max_pages)
        binding_data = {
            "Pocket Book (4.25 x 6.87 in)": [
                ("Perfect Bound", 1.60, 32, 470),
                ("Saddle Stitch", 3.00, 4, 48),
                ("Case Wrap", 7.00, 24, 470),
                ("Coil Bound", 4.50, 3, 470),
                ("Linen Wrap", 10.00, 32, 470),
            ],
            "Digest (5.5 x 8.5 in)": [
                ("Perfect Bound", 1.80, 32, 470),
                ("Saddle Stitch", 3.50, 4, 48),
                ("Case Wrap", 8.50, 24, 470),
                ("Coil Bound", 5.50, 3, 470),
                ("Linen Wrap", 12.00, 32, 470),
            ],
            "US Trade (6 x 9 in)": [
                ("Perfect Bound", 2.00, 32, 470),
                ("Saddle Stitch", 3.90, 4, 48),
                ("Case Wrap", 10.00, 24, 470),
                ("Coil Bound", 6.50, 3, 470),
                ("Linen Wrap", 14.00, 32, 470),
            ],
            "Royal (6.14 x 9.21 in)": [
                ("Perfect Bound", 2.10, 32, 470),
                ("Saddle Stitch", 4.00, 4, 48),
                ("Case Wrap", 10.50, 24, 470),
                ("Coil Bound", 6.80, 3, 470),
                ("Linen Wrap", 14.50, 32, 470),
            ],
            "US Letter (8.5 x 11 in)": [
                ("Perfect Bound", 2.50, 32, 470),
                ("Saddle Stitch", 4.30, 4, 48),
                ("Case Wrap", 11.00, 24, 470),
                ("Coil Bound", 7.00, 3, 470),
                ("Linen Wrap", 15.00, 32, 470),
            ],
            "Square (8.5 x 8.5 in)": [
                ("Perfect Bound", 2.30, 32, 470),
                ("Saddle Stitch", 4.10, 4, 48),
                ("Case Wrap", 10.80, 24, 470),
                ("Coil Bound", 6.90, 3, 470),
                ("Linen Wrap", 14.80, 32, 470),
            ],
            "A4": [
                ("Perfect Bound", 2.00, 32, 470),
                ("Saddle Stitch", 3.82, 4, 48),
                ("Case Wrap", 9.75, 24, 470),
                ("Coil Bound", 6.18, 3, 470),
                ("Linen Wrap", 13.80, 32, 470),
            ],
            "A5": [
                ("Perfect Bound", 1.70, 32, 470),
                ("Saddle Stitch", 3.20, 4, 48),
                ("Case Wrap", 8.00, 24, 470),
                ("Coil Bound", 5.00, 3, 470),
                ("Linen Wrap", 11.00, 32, 470),
            ],
            "Executive (7 x 10 in)": [
                ("Perfect Bound", 2.20, 32, 470),
                ("Saddle Stitch", 4.20, 4, 48),
                ("Case Wrap", 11.20, 24, 470),
                ("Coil Bound", 7.20, 3, 470),
                ("Linen Wrap", 15.20, 32, 470),
            ],
            "Crown Quarto (7.44 x 9.68 in)": [
                ("Perfect Bound", 2.15, 32, 470),
                ("Saddle Stitch", 4.05, 4, 48),
                ("Case Wrap", 10.90, 24, 470),
                ("Coil Bound", 7.10, 3, 470),
                ("Linen Wrap", 14.90, 32, 470),
            ],
            "Novella (5 x 8 in)": [
                ("Perfect Bound", 1.90, 32, 470),
                ("Saddle Stitch", 3.60, 4, 48),
                ("Case Wrap", 9.00, 24, 470),
                ("Coil Bound", 6.00, 3, 470),
                ("Linen Wrap", 13.00, 32, 470),
            ],
        }

        for trim_name, bindings in binding_data.items():
            trim_obj = trim_sizes[trim_name]['obj']
            for name, price, min_pages, max_pages in bindings:
                BindingType.objects.get_or_create(
                    name=name,
                    price=price,
                    trim_size=trim_obj,
                    min_pages=min_pages,
                    max_pages=max_pages
                )

        self.stdout.write(self.style.SUCCESS("✅ All trim sizes and binding types seeded as per calculation table!"))
