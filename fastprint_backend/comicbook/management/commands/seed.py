from django.core.management.base import BaseCommand
from comicbook.models import (
    ComicTrimSize,
    ComicBindingType,
    ComicInteriorColor,
    ComicPaperType,
    ComicCoverFinish
)

class Command(BaseCommand):
    help = "Seeds the database with Comic Book data"

    def handle(self, *args, **kwargs):
        # Trim Sizes
        comic = ComicTrimSize.objects.get_or_create(name="Comic Book (6.625 x 10.25 in)")[0]
        deluxe = ComicTrimSize.objects.get_or_create(name="Larger Deluxe (7 x 10.875 in)")[0]
        manga = ComicTrimSize.objects.get_or_create(name="Manga (5 x 7.5 in)")[0]

        # Interior Colors
        ComicInteriorColor.objects.get_or_create(name="Premium Black & White", price_per_page=0.03)
        ComicInteriorColor.objects.get_or_create(name="Premium Color", price_per_page=0.19)

        # Paper Types
        ComicPaperType.objects.get_or_create(name="70# White-Uncoated", price_per_page=0.02)
        ComicPaperType.objects.get_or_create(name="60# Cream-Uncoated", price_per_page=0.01)
        ComicPaperType.objects.get_or_create(name="60# White-Uncoated", price_per_page=0.01)
        ComicPaperType.objects.get_or_create(name="80# White-Coated", price_per_page=0.03)

        # Cover Finishes
        ComicCoverFinish.objects.get_or_create(name="Gloss", price=0.00)
        ComicCoverFinish.objects.get_or_create(name="Matte", price=0.00)

        # Bindings for Comic Book size
        ComicBindingType.objects.get_or_create(name="Perfect Bound", price=2.50, trim_size=comic, min_pages=32)
        ComicBindingType.objects.get_or_create(name="Saddle Stitch", price=5.00, trim_size=comic, min_pages=4, max_pages=48)
        ComicBindingType.objects.get_or_create(name="Case Wrap", price=9.75, trim_size=comic, min_pages=24)
        ComicBindingType.objects.get_or_create(name="Linen Wrap", price=13.80, trim_size=comic, min_pages=32)
        ComicBindingType.objects.get_or_create(name="Coil Bound", price=6.18, trim_size=comic, min_pages=3, max_pages=470)

        # Bindings for Larger Deluxe size
        ComicBindingType.objects.get_or_create(name="Perfect Bound", price=3.00, trim_size=deluxe, min_pages=32)
        ComicBindingType.objects.get_or_create(name="Saddle Stitch", price=5.00, trim_size=deluxe, min_pages=4, max_pages=48)
        ComicBindingType.objects.get_or_create(name="Case Wrap", price=9.75, trim_size=deluxe, min_pages=24)
        ComicBindingType.objects.get_or_create(name="Linen Wrap", price=13.80, trim_size=deluxe, min_pages=32)
        ComicBindingType.objects.get_or_create(name="Coil Bound", price=6.18, trim_size=deluxe, min_pages=3, max_pages=470)

        # Bindings for Manga size
        ComicBindingType.objects.get_or_create(name="Perfect Bound", price=2.50, trim_size=manga, min_pages=32)
        ComicBindingType.objects.get_or_create(name="Saddle Stitch", price=5.00, trim_size=manga, min_pages=4, max_pages=48)
        ComicBindingType.objects.get_or_create(name="Case Wrap", price=9.75, trim_size=manga, min_pages=24)
        ComicBindingType.objects.get_or_create(name="Linen Wrap", price=13.80, trim_size=manga, min_pages=32)
        ComicBindingType.objects.get_or_create(name="Coil Bound", price=6.18, trim_size=manga, min_pages=3, max_pages=470)

        self.stdout.write(self.style.SUCCESS("✅ Comic Book sample data seeded."))
