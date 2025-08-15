from django.core.management.base import BaseCommand
from magazine.models import TrimSize, InteriorColor, PaperType, BindingType, CoverFinish

class Command(BaseCommand):
    help = 'Seed initial magazine data'

    def handle(self, *args, **kwargs):
        # Trim Sizes
        TrimSize.objects.get_or_create(name="A4 (8.27 x 11.69 in / 210 x 297 mm)")
        TrimSize.objects.get_or_create(name="US Letter (8.5 x 11 in / 216 x 279 mm)")

        # Interior Colors
        InteriorColor.objects.get_or_create(name="Premium Black & white", price_per_page=0.0325)
        InteriorColor.objects.get_or_create(name="Premium Color", price_per_page=0.19)

        # Paper Types
        PaperType.objects.get_or_create(name="70# White-Uncoated", price_per_page=0.02)
        PaperType.objects.get_or_create(name="60# Cream-Uncoated", price_per_page=0.01)
        PaperType.objects.get_or_create(name="60# White-uncoated", price_per_page=0.01)
        PaperType.objects.get_or_create(name="80# White-Coated", price_per_page=0.03)

        # Cover Finish (if applicable)
        CoverFinish.objects.get_or_create(name="Gloss", price=0.00)
        CoverFinish.objects.get_or_create(name="Matte", price=0.00)

        # Binding Types with Prices
        BindingType.objects.get_or_create(name="Perfect bond", price=2.50)
        BindingType.objects.get_or_create(name="Saddle Stitch", price=5.00)
        BindingType.objects.get_or_create(name="Case Wrap", price=9.75)
        BindingType.objects.get_or_create(name="Linen Wrap", price=13.80)
        BindingType.objects.get_or_create(name="Coil Bond", price=6.18)

        self.stdout.write(self.style.SUCCESS('✅ Magazine seed data loaded successfully.'))
