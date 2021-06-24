from django.contrib import admin
from .models import Author, Post, Tag, Comment
# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'updated_date',)
    list_filter = ('author', 'tag', 'updated_date')
    prepopulated_fields = {'slug': ('title',)}


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'comment_text')
    


admin.site.register(Post, PostAdmin)
admin.site.register(Author)
admin.site.register(Tag)
admin.site.register(Comment, CommentAdmin)
