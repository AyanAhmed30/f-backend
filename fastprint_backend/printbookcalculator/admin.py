from django.contrib import admin
from .models import TrimSize, BindingType, InteriorColor, PaperType, CoverFinish

admin.site.register(TrimSize)
admin.site.register(BindingType)
admin.site.register(InteriorColor)
admin.site.register(PaperType)
admin.site.register(CoverFinish)
