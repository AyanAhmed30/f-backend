from django.db import models

class ComicTrimSize(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ComicBindingType(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    trim_size = models.ForeignKey(ComicTrimSize, on_delete=models.CASCADE)
    min_pages = models.IntegerField(default=1)
    max_pages = models.IntegerField(default=9999, null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.trim_size.name}"


class ComicInteriorColor(models.Model):
    name = models.CharField(max_length=100)
    price_per_page = models.DecimalField(max_digits=5, decimal_places=3)

    def __str__(self):
        return self.name


class ComicPaperType(models.Model):
    name = models.CharField(max_length=100)
    price_per_page = models.DecimalField(max_digits=5, decimal_places=3)

    def __str__(self):
        return self.name


class ComicCoverFinish(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name
