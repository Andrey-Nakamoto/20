from django.contrib import admin
from .models import Author, Post, Comment, Category
class PostAdmin(admin.ModelAdmin):
    list_display = ('titles','posttext', 'author')
    list_filter = ('titles','posttext', 'author')
    search_fields = ('titles', 'category__name')


admin.site.register(Author)
admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Comment)

