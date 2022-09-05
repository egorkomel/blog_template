from django.contrib import admin
from .models import Post, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'tag', 'created_at')
    list_filter = ('author', 'tag', 'created_at')


admin.site.register(Post, PostAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('username', 'post', 'text', 'created_at')
    list_filter = ('username', 'created_at')


admin.site.register(Comment, CommentAdmin)
