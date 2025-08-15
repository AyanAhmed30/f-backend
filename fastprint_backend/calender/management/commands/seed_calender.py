from django.core.management.base import BaseCommand
from calender.models import BindingType, InteriorColor, PaperType, CoverFinish

class Command(BaseCommand):
    help = 'Seed data for Calendar Calculator'

    def handle(self, *args, **kwargs):
        BindingType.objects.all().delete()
        InteriorColor.objects.all().delete()
        PaperType.objects.all().delete()
        CoverFinish.objects.all().delete()

        BindingType.objects.create(name='Wire O', price=12.00)
        InteriorColor.objects.create(name='Premium Color', price=0.00)
        PaperType.objects.create(name='100# White-Coated', price=0.00)
        CoverFinish.objects.create(name='Gloss', price=0.00)
        CoverFinish.objects.create(name='Matte', price=0.00)

        self.stdout.write(self.style.SUCCESS("📘 Calendar seed data added successfully!"))
