# , NewPost, PostDetails, tags, like, favorite
from posts.views import index, temp_conversation, temp_notifications, temp_profile
from django.urls import path


urlpatterns = [
    path('', index, name='index'),
    path('direct/', temp_conversation, name='temporatio_direct'),
    path('notifications/', temp_notifications, name='temporatio_notifications'),
    path('profile/', temp_profile, name='temp_profile'),
    # path('newpost/', NewPost, name='newpost'),
    # path('<uuid:post_id>/', PostDetails, name='postdetails'),
    # path('tag/<slug:tag_slug>', tags, name='tags'),
    # path('<uuid:post_id>/like', like, name='postlike'),
    # path('<uuid:post_id>/favorite', favorite, name='postfavorite'),
]
