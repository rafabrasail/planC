from django.contrib import admin
from posts.models import Post, Tag, Follow, Stream, PostFileContent


admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Follow)
admin.site.register(Stream)
admin.site.register(PostFileContent)
