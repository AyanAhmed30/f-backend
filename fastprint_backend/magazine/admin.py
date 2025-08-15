from django.contrib import admin
from .models import TrimSize, InteriorColor, PaperType, BindingType, CoverFinish

admin.site.register(TrimSize)
admin.site.register(InteriorColor)
admin.site.register(PaperType)
admin.site.register(BindingType)
admin.site.register(CoverFinish)
