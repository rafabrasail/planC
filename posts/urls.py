# NewPost, PostDetails, tags, like, favorite
from django.urls import path
from .views import (
    list_and_create_posts,
    load_posts,
    like_unlike_post,
    PostDetails,
    post_detail_json,
    update_posts,
    delete_posts,
    NewPost,
    tags
)

app_name = 'posts'

urlpatterns = [
    path('', list_and_create_posts, name='main-board'),
    path('create-post/', NewPost, name='create-post'),
    path('posts/', load_posts, name='posts-data'),
    path('tag/<slug:tag_slug>', tags, name='tags'),
    path('like-unlike/', like_unlike_post, name='like-unlike'),
    path('<pk>/data/', post_detail_json, name='posts-detail-json'),
    path('<uuid:post_id>/', PostDetails, name='postdetails'),
    path('<pk>/update/', update_posts, name='update-post'),
    path('<pk>/delete/', delete_posts, name='delete-post'),
    
    # path('notifications/', temp_notifications, name='temporatio_notifications'),
    # path('profile/', temp_profile, name='temp_profile'),
    # path('newpost/', NewPost, name='newpost'),
    # path('<uuid:post_id>/', PostDetails, name='postdetails'),
    # path('tag/<slug:tag_slug>', tags, name='tags'),
    # path('<uuid:post_id>/like', like, name='postlike'),
    # path('<uuid:post_id>/favorite', favorite, name='postfavorite'),
]
