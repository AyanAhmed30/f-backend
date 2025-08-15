from django.db import models
from django.conf import settings

class TrimSize(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class BindingType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class InteriorColor(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class PaperType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class CoverFinish(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class BookProject(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='book_projects')
    title = models.CharField(max_length=255)
    language = models.CharField(max_length=50, blank=True, null=True)
    category = models.CharField(max_length=100)
    pdf_file = models.FileField(upload_to='books/pdfs/')
    cover_file = models.FileField(upload_to='books/covers/', blank=True, null=True)
    page_count = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    # Store these as strings, not foreign keys
    binding_type = models.CharField(max_length=100, blank=True, null=True)
    cover_finish = models.CharField(max_length=100, blank=True, null=True)
    interior_color = models.CharField(max_length=100, blank=True, null=True)
    paper_type = models.CharField(max_length=100, blank=True, null=True)
    trim_size = models.CharField(max_length=100, blank=True, null=True)

    # ✅ New field for cover design description
    cover_description = models.TextField(blank=True, null=True)
    

    def __str__(self):
        return f"{self.title} by {self.user.email}"
