from django.db import models

class TrimSize(models.Model):
    name = models.CharField(max_length=100)

class BindingType(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)

class InteriorColor(models.Model):
    name = models.CharField(max_length=100)
    price_per_page = models.DecimalField(max_digits=6, decimal_places=4)

class PaperType(models.Model):
    name = models.CharField(max_length=100)
    price_per_page = models.DecimalField(max_digits=6, decimal_places=4)

class CoverFinish(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0)