from django.contrib import admin
from .models import (
    ComicTrimSize,
    ComicBindingType,
    ComicInteriorColor,
    ComicPaperType,
    ComicCoverFinish,
)

admin.site.register(ComicTrimSize)
admin.site.register(ComicBindingType)
admin.site.register(ComicInteriorColor)
admin.site.register(ComicPaperType)
admin.site.register(ComicCoverFinish)
