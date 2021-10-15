from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from posts.models import Post, Stream, Tag, Likes, PostFileContent
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from posts.forms import NewPostForm
from django.urls import reverse
from author.models import Profile
# from comment.models import Comment
# from comment.forms import CommentForm
# from stories.models import Story, StoryStream


@login_required
def index(request):
    user = request.user
    posts = Stream.objects.filter(user=user)

    # stories = StoryStream.objects.filter(user=user)

    group_ids = []
    for post in posts:
        group_ids.append(post.post_id)

    post_items = Post.objects.filter(
        id__in=group_ids).all().order_by('-posted')

    template = loader.get_template('mainpage.html')

    context = {
        'post_items': post_items,
        # 'stories': stories,
    }

    return HttpResponse(template.render(context, request))
