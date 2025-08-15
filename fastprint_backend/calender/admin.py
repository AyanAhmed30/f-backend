from django.contrib import admin
from .models import BindingType, InteriorColor, PaperType, CoverFinish

admin.site.register(BindingType)
admin.site.register(InteriorColor)
admin.site.register(PaperType)
admin.site.register(CoverFinish)
