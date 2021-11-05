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


    tags_objs = []
    files_objs = []

    if request.method == "POST":
        form = NewPostForm(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist('content')
            caption = form.cleaned_data.get('caption')
            tags_form = form.cleaned_data.get('tags')

            tags_list = list(tags_form.split(','))

            for tag in tags_list:
                t, created = Tag.objects.get_or_create(title=tag)
                tags_objs.append(t)

            for file in files:
                file_instance = PostFileContent(file=file, user=user)
                file_instance.save()
                files_objs.append(file_instance)

            p, created = Post.objects.get_or_create(caption=caption, user=user)
            p.tags.set(tags_objs)
            p.content.set(files_objs)
            p.save()
            return redirect('index')
    else:
        form = NewPostForm()


    template = loader.get_template('mainpage.html')

    context = {
        'post_items': post_items,
        # 'stories': stories,
        'form': form,
    }

    return HttpResponse(template.render(context, request))


@login_required
def NewPost(request):
    user = request.user
    tags_objs = []
    files_objs = []

    if request.method == "POST":
        form = NewPostForm(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist('content')
            caption = form.cleaned_data.get('caption')
            tags_form = form.cleaned_data.get('tags')

            tags_list = list(tags_form.split(','))

            for tag in tags_list:
                t, created = Tag.objects.get_or_create(title=tag)
                tags_objs.append(t)

            for file in files:
                file_instance = PostFileContent(file=file, user=user)
                file_instance.save()
                files_objs.append(file_instance)

            p, created = Post.objects.get_or_create(caption=caption, user=user)
            p.tags.set(tags_objs)
            p.content.set(files_objs)
            p.save()
            return redirect('index')
    else:
        form = NewPostForm()

    context = {
        'form': form,
    }

    return render(request, 'mainpage.html', context)


def temp_conversation(request):
    template = loader.get_template('conversations.html')
    context = {}
    return HttpResponse(template.render(context,request))


def temp_notifications(request):
    template = loader.get_template('notifications.html')
    context = {}
    return HttpResponse(template.render(context,request))


def temp_profile(request):
    template = loader.get_template('profile.html')
    context = {}
    return HttpResponse(template.render(context,request))    