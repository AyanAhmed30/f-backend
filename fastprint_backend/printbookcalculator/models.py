from django.db import models


class TrimSize(models.Model):
    name = models.CharField(max_length=100)  # e.g. A5, US Letter
    # e.g. 5 x 8 in / 127 x 203 mm
    dimensions = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class BindingType(models.Model):
    # Perfect Bound, Saddle Stitch, etc.
    name = models.CharField(max_length=100)
    trim_size = models.ForeignKey(TrimSize, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    min_pages = models.IntegerField(default=0)  # ✅ Add this
    max_pages = models.IntegerField(default=10000)  # ✅ And this

    def __str__(self):
        return f"{self.name} - {self.trim_size.name}"


class InteriorColor(models.Model):
    # Standard B&W, Premium Color, etc.
    name = models.CharField(max_length=100)
    price_per_page = models.DecimalField(max_digits=5, decimal_places=4)

    def __str__(self):
        return self.name


class PaperType(models.Model):
    # 60# Cream-Uncoated, 80# White-Coated
    name = models.CharField(max_length=100)
    price_per_page = models.DecimalField(max_digits=5, decimal_places=4)

    def __str__(self):
        return self.name


class CoverFinish(models.Model):
    name = models.CharField(max_length=100)  # Matte, Gloss
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name
