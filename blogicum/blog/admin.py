from django.contrib import admin

from .models import Category, Location, Post

OBJECT_PER_PAGE: int = 10


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Управление тематическими категориями."""
    list_display = [
        'title',
        'description',
        'is_published'
    ]
    list_editable = [
        'description',
        'is_published'
    ]
    list_per_page = OBJECT_PER_PAGE
    ordering = [
        'title',
        'description'
    ]


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    """Управление геогрофическими метками."""
    list_display = [
        'name',
        'is_published'
    ]
    list_editable = [
        'is_published'
    ]
    list_per_page = OBJECT_PER_PAGE
    ordering = [
        'name',
        'created_at'
    ]


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Управление публикациями."""
    list_display = [
        'title',
        'text',
        'location',
        'pub_date',
        'category',
        'is_published'
    ]
    list_editable = [
        'text',
        'location',
        'pub_date',
        'category',
        'is_published'
    ]
    list_per_page = OBJECT_PER_PAGE
    ordering = [
        '-pub_date',
        'title'
    ]
