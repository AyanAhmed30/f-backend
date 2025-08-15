
# yearbook/models.py
from django.db import models

class TrimSize(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class BindingType(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class InteriorColor(models.Model):
    name = models.CharField(max_length=100)
    price_per_page = models.DecimalField(max_digits=10, decimal_places=4)

    def __str__(self):
        return self.name


class PaperType(models.Model):
    name = models.CharField(max_length=100)
    price_per_page = models.DecimalField(max_digits=10, decimal_places=4)

    def __str__(self):
        return self.name


class CoverFinish(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return self.name

