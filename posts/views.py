from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, Stream, Tag, PostFileContent
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from posts.forms import NewPostForm
from django.urls import reverse
from author.models import Profile
from django.views.decorators.csrf import csrf_exempt
# from comment.models import Comment
# from comment.forms import CommentForm
# from stories.models import Story, StoryStream


@login_required
def list_and_create_posts(request):
    qs = Post.objects.all()
    return render(request, 'posts/mainpage.html', {'qs': qs})


@login_required
def load_posts(request):
    qs = Post.objects.all()
    data = []
    for obj in qs:
        item = {
            'id': obj.id,
            'caption': obj.caption,
            'posted': obj.posted,
            'liked': True if request.user in obj.liked.all() else False,
            'user': obj.user.username,
            'count': obj.like_count,
        }
        data.append(item)
    return JsonResponse({'data': data})


@login_required
def like_unlike_post(request):
    if request.is_ajax():
        pk = request.POST.get('pk')
        obj = Post.objects.get(pk=pk)
        if request.user.profile in obj.liked.all():
            liked = False
            obj.liked.remove(request.user.profile)
        else:
            liked = True
            obj.liked.add(request.user.profile)
        return JsonResponse({'liked': liked, 'count': obj.like_count})



# @login_required
# def load_posts(request):
#     if request.is_ajax():
#         visible = 3
#         # upper = num_posts
#         # lower = upper - visible
#         size = Post.objects.all().count()

#         qs = Post.objects.all()
#         data = []
#         for obj in qs:
#             item = {
#                 'id': obj.id,
#                 'caption': obj.caption,
#                 'posted': obj.posted
#             }
#             data.append(item)
#         return JsonResponse({
#             'data': data,
#             'size': size})


# @login_required
# def index(request):
#     user = request.user
#     posts = Stream.objects.filter(user=user)

#     # stories = StoryStream.objects.filter(user=user)

#     group_ids = []
#     for post in posts:
#         group_ids.append(post.post_id)

#     post_items = Post.objects.filter(
#         id__in=group_ids).all().order_by('-posted')


#     # tags_objs = []
#     # files_objs = []

#     # if request.method == "POST":
#     #     form = NewPostForm(request.POST, request.FILES)
#     #     if form.is_valid():
#     #         files = request.FILES.getlist('content')
#     #         caption = form.cleaned_data.get('caption')
#     #         tags_form = form.cleaned_data.get('tags')

#     #         tags_list = list(tags_form.split(','))

#     #         for tag in tags_list:
#     #             t, created = Tag.objects.get_or_create(title=tag)
#     #             tags_objs.append(t)

#     #         for file in files:
#     #             file_instance = PostFileContent(file=file, user=user)
#     #             file_instance.save()
#     #             files_objs.append(file_instance)

#     #         p, created = Post.objects.get_or_create(caption=caption, user=user)
#     #         p.tags.set(tags_objs)
#     #         p.content.set(files_objs)
#     #         p.save()
#     #         return redirect('index')
#     # else:
#     #     form = NewPostForm()


#     template = loader.get_template('mainpage.html')

#     context = {
#         'post_items': post_items,
#         # 'stories': stories,
#         # 'form': form,
#     }

#     return HttpResponse(template.render(context, request))


# @login_required
# @csrf_exempt
# def NewPost(request):

#     form = NewPostForm(request.POST or None)
#     if request.is_ajax():
#         if form.is_valid():

#             instance = form.save()

#             return JsonResponse({
#                 'caption': instance.caption,
#             })

#     context={
#         'form': form,
#     }

#     return render(request, 'posts/create_post.html', context)




# @login_required
# def NewPost(request):
#     user = request.user
#     tags_objs = []
#     files_objs = []

#     if request.method == "POST":
#         form = NewPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             files = request.FILES.getlist('content')
#             caption = form.cleaned_data.get('caption')
#             tags_form = form.cleaned_data.get('tags')

#             tags_list = list(tags_form.split(','))

#             for tag in tags_list:
#                 t, created = Tag.objects.get_or_create(title=tag)
#                 tags_objs.append(t)

#             for file in files:
#                 file_instance = PostFileContent(file=file, user=user)
#                 file_instance.save()
#                 files_objs.append(file_instance)

#             p, created = Post.objects.get_or_create(caption=caption, user=user)
#             p.tags.set(tags_objs)
#             p.content.set(files_objs)
#             p.save()
#             return redirect('index')
#     else:
#         form = NewPostForm()

#     context = {
#         'form': form,
#     }

#     return render(request, 'mainpage.html', context)


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
