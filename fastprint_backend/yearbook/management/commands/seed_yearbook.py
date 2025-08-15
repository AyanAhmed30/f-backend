from django.core.management.base import BaseCommand
from yearbook.models import TrimSize, BindingType, InteriorColor, PaperType, CoverFinish

class Command(BaseCommand):
    help = 'Seed data for YearBookCalculator'

    def handle(self, *args, **kwargs):
        # Clear existing data
        TrimSize.objects.all().delete()
        BindingType.objects.all().delete()
        InteriorColor.objects.all().delete()
        PaperType.objects.all().delete()
        CoverFinish.objects.all().delete()

        # Trim Sizes
        trim_sizes = [
            "A4 (8.27 x 11.69 in / 210 x 297 mm)",
            "US Letter (8.5 x 11 in / 216 x 279 mm)",
            "US Letter Landscape (11 x 8.5 in / 279 x 216 mm)",
            "A4 Landscape (11.69 x 8.27 in / 297 x 210 mm)"
        ]
        for name in trim_sizes:
            TrimSize.objects.create(name=name)

        # Binding Types
        bindings = [
            ("Perfect bond", 2.50),
            ("Saddle Stitch", 5.00),
            ("Case Wrap", 9.75),
            ("Linen Wrap", 13.80),
            ("coil bond", 6.18),
        ]
        for name, price in bindings:
            BindingType.objects.create(name=name, price=price)

        # Interior Colors
        interior_colors = [
            ("Premium Black & white", 0.03),
            ("Premium Color", 0.19),
        ]
        for name, price_per_page in interior_colors:
            InteriorColor.objects.create(name=name, price_per_page=price_per_page)

        # Paper Types
        paper_types = [
            ("70# White-Uncoated", 0.02),
            ("60# Cream-Uncoated", 0.01),
            ("60# White-uncoated", 0.01),
            ("80# White-Coated", 0.03),
        ]
        for name, price_per_page in paper_types:
            PaperType.objects.create(name=name, price_per_page=price_per_page)

        # Cover Finishes
        cover_finishes = [
            ("Gloss", 0.00),
            ("Matte", 0.00),
        ]
        for name, price in cover_finishes:
            CoverFinish.objects.create(name=name, price=price)

        self.stdout.write(self.style.SUCCESS('✅ YearBookCalculator data seeded successfully.'))
