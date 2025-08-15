from django.core.management.base import BaseCommand
from photobook.models import (
    TrimSize, BindingType, Spine, ExteriorColor, FoilStamping, ScreenStamping,
    CornerProtector, InteriorColor, PaperType
)

class Command(BaseCommand):
    help = 'Seeds Photobook Calculator data based on formula sheet'

    def handle(self, *args, **kwargs):
        # Trim Sizes (extracted from formula sheet)
        TrimSize.objects.bulk_create([
            TrimSize(name="Pocket Book (4.25 x 6.875 in / 108 x 175 mm)"),
            TrimSize(name="Novella (5 x 8 in / 127 x 203 mm)"),
            TrimSize(name="Digest (5.5 x 8.5 in / 140 x 216 mm)"),
            TrimSize(name="A5 (5.83 x 8.27 in / 148 x 210 mm)"),
            TrimSize(name="US Trade (6 x 9 in / 152 x 229 mm)"),
            TrimSize(name="Royal (6.14 x 9.21 in / 156 x 234 mm)"),
            TrimSize(name="Executive (7 x 10 in / 178 x 254 mm)"),
            TrimSize(name="Crown Quarto (7.44 x 9.68 in / 189 x 246 mm)"),
            TrimSize(name="Small Square (7.5 x 7.5 in / 190 x 190 mm)"),
            TrimSize(name="A4 (8.27 x 11.69 in / 210 x 297 mm)"),
            TrimSize(name="Square (8.5 x 8.5 in / 216 x 216 mm)"),
            TrimSize(name="US Letter (8.5 x 11 in / 216 x 279 mm)"),
            TrimSize(name="Small Landscape (9 x 7 in / 229 x 178 mm)"),
            TrimSize(name="US Letter Landscape (11 x 8.5 in / 279 x 216 mm)"),
        ])

        # Binding Types
        BindingType.objects.bulk_create([
            BindingType(name="Perfect Bond", price=2.00),  # Update prices as needed per trim
            BindingType(name="Case Wrap", price=9.50),
            BindingType(name="Linen Wrap", price=14.00),
        ])

        # Spines
        Spine.objects.bulk_create([
            Spine(name="Flat", price=0),
            Spine(name="Round", price=5),
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

        # Corner Protectors (Optional for Photobook UI)
        CornerProtector.objects.bulk_create([
            CornerProtector(name="Gold Sharp Corner", price=4, image_url="https://www.amazon.com/Concise-Corner-Protector-Simple-Guarder/dp/B07RK9KNF2"),
            CornerProtector(name="Gold Round Corner", price=4, image_url="https://www.amazon.com/Scrapbooking-Mounting-Corners-Notebook-Protectors/dp/B07MC49Z25"),
            CornerProtector(name="Vintage Designs Corner", price=6, image_url="https://www.amazon.com/Protector-Triangle-Decorative-Vintage-Scrapbooking/dp/B09X1LXBR2"),
        ])

        # Interior Colors (from sheet)
        InteriorColor.objects.bulk_create([
            InteriorColor(name="Premium Black & white", price_per_page=0.03),
            InteriorColor(name="Premium Color", price_per_page=0.17),
        ])

        # Paper Types (match exact rates from formula)
        PaperType.objects.bulk_create([
            PaperType(name="80# White-Coated", price_per_page=0.015),
        ])

        self.stdout.write(self.style.SUCCESS("✅ PhotoBook Calculator options seeded as per formula sheet."))
