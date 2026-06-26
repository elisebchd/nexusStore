from django.contrib import admin
from .models import Post, BlogCategory


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'views', 'published_at']
    list_filter = ['status', 'category']
    list_editable = ['status']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        ('Content', {'fields': ('title', 'slug', 'author', 'category', 'excerpt', 'content', 'featured_image')}),
        ('Publishing', {'fields': ('status', 'published_at')}),
        ('SEO', {'fields': ('meta_description',)}),
    )
