from django.db import models

class BindingType(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class SpineType(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)

class ExteriorColor(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)

class FoilStamping(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)

class ScreenStamping(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)

class CornerProtector(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

class InteriorColor(models.Model):
    name = models.CharField(max_length=100)
    price_per_page = models.DecimalField(max_digits=10, decimal_places=4)

class PaperType(models.Model):
    name = models.CharField(max_length=100)
    price_per_page = models.DecimalField(max_digits=10, decimal_places=4)
