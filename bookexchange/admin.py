from django.contrib import admin
from .models import Book, Comment, Discussion, Review
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _



@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_cover_image')
    search_fields = ('title', 'author')

    def display_cover_image(self, obj):
        return mark_safe(f'<img src="{obj.cover_image.url}" width="110" height="150" />')

    display_cover_image.short_description = _("Image")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('book', 'text', 'created_at')
    list_filter = ('book', 'created_at')
    search_fields = ('text', 'user__email')



@admin.register(Discussion)
class DiscussionAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('book', 'rating', 'created_at')
    search_fields = ('book__title',)
