# book/admin.py
from django.contrib import admin
from .models import BookProject

@admin.register(BookProject)
class BookProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_user_email', 'category', 'language', 'page_count', 'created_at',
                    'binding_type', 'cover_finish', 'interior_color', 'paper_type', 'trim_size')

    def get_user_email(self, obj):
        return obj.user.email
    get_user_email.short_description = 'User Email'
