from django.contrib import admin
from .models import BlogPost

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_date', 'views')
    search_fields = ('title',)

admin.site.register(BlogPost, BlogPostAdmin)
