from django.core.management.base import BaseCommand
from photobook.models import (
    TrimSize, BindingType, Spine, ExteriorColor, FoilStamping, ScreenStamping,
    CornerProtector, InteriorColor, PaperType
)

class Command(BaseCommand):
    help = 'Seeds Photobook Calculator data'

    def handle(self, *args, **kwargs):
        # Trim Sizes
        TrimSize.objects.bulk_create([
            TrimSize(name="A4 (8.27 x 11.69 in / 210 x 297 mm)"),
            TrimSize(name="Comic Book (6.625 x 10.25 in / 168 x 260 mm)"),
            TrimSize(name="US Letter (8.5 x 11 in / 216 x 279 mm)")
        ])

        # Bindings
        BindingType.objects.bulk_create([
            BindingType(name="Leather Case Wrap", price=79),
            BindingType(name="Faux Leather Case Wrap", price=69),
            BindingType(name="Polythin Rexine Case Wrap", price=59),
        ])

        # Spines
        Spine.objects.bulk_create([
            Spine(name="Round", price=5),
            Spine(name="Flat", price=0),
        ])

        # Exterior Colors
        ExteriorColor.objects.bulk_create([
            ExteriorColor(name="Black", price=5),
            ExteriorColor(name="Brown", price=3),
            ExteriorColor(name="Maroon", price=5),
            ExteriorColor(name="Dark Blue", price=5),
        ])

        # Foil Stamping
        FoilStamping.objects.bulk_create([
            FoilStamping(name="Golden", price=10),
            FoilStamping(name="Silver", price=15),
        ])

        # Screen Stamping
        ScreenStamping.objects.bulk_create([
            ScreenStamping(name="Golden", price=10),
            ScreenStamping(name="Silver", price=15),
        ])

        # Corner Protectors
        CornerProtector.objects.bulk_create([
            CornerProtector(name="Gold Sharp Corner", price=4, image_url="https://www.amazon.com/Concise-Corner-Protector-Simple-Guarder/dp/B07RK9KNF2"),
            CornerProtector(name="Gold Round Corner", price=4, image_url="https://www.amazon.com/Scrapbooking-Mounting-Corners-Notebook-Protectors/dp/B07MC49Z25"),
            CornerProtector(name="Vintage Designs Corner", price=6, image_url="https://www.amazon.com/Protector-Triangle-Decorative-Vintage-Scrapbooking/dp/B09X1LXBR2"),
        ])

        # Interior Colors
        InteriorColor.objects.bulk_create([
            InteriorColor(name="Premium Black & white", price_per_page=0.03),
            InteriorColor(name="Premium Color", price_per_page=0.19),
        ])

        # Paper Types
        PaperType.objects.bulk_create([
            PaperType(name="70# White-Uncoated", price_per_page=0.02),
            PaperType(name="60# Cream-Uncoated", price_per_page=0.01),
            PaperType(name="60# White-uncoated", price_per_page=0.01),
            PaperType(name="80# White-Coated", price_per_page=0.03),
        ])

        self.stdout.write(self.style.SUCCESS('✅ Photobook options seeded successfully.'))
