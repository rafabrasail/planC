from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, Stream, Tag, PostFileContent
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from .forms import NewPostForm
from django.urls import reverse

from django.views.decorators.csrf import csrf_exempt
# from comment.models import Comment
# from comment.forms import CommentForm
# from stories.models import Story, StoryStream


@login_required
@csrf_exempt
def list_and_create_posts(request):
    user = request.user
    posts = Stream.objects.filter(user=user)

    group_ids = []
    for post in posts:
        group_ids.append(post.post_id)

    post_items = Post.objects.filter(
        id__in=group_ids).all().order_by('-posted')


    template = loader.get_template('posts/mainpage.html')

    context = {
        'post_items': post_items,
    }

    return HttpResponse(template.render(context, request))




# @login_required     backup
# @csrf_exempt
# def list_and_create_posts(request):
#         form = NewPostForm(request.POST, request.FILES)
#         if request.is_ajax():
#             if form.is_valid():
#                 instance = form.save(commit=False)
#                 instance.user = request.user
#                 instance.save()
#                 return JsonResponse({
#                     'caption': instance.caption,
#                     'id': instance.id
#                 })

#     context = {
#         'form': form,
#     }
#     return render(request, 'posts/mainpage.html', context)


@login_required
def NewPost(request):
    user = request.user
    tags_objs = []
    files_objs = []

    if request.method == "POST":
        form = NewPostForm(request.POST, request.FILES)
        if form.is_valid():
            # picture = form.cleaned_data.get('picture')
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
            return redirect('posts:main-board')
    else:
        form = NewPostForm()
    
    context = {
        'form': form,
    }

    return render(request, 'posts/new_posts.html', context)


# função para carregar os posts na mainpage usando o getData JS para 
# injetar os posts na página. O Stream é inserido aqui para exibir 
# somente os conteúdos dos seguidores. 
@login_required
def load_posts(request):
    if request.is_ajax():
        user = request.user
        posts = Stream.objects.filter(user=user)
        group_ids = []
        for post in posts:
            group_ids.append(post.post_id)

        post_items = Post.objects.filter(
            id__in=group_ids).all().order_by('-posted')

        data = []
        for obj in post_items:
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


# TODO: testar função para todos os posts (REELS) no DB
# def reels(request):
#     if request.is_ajax():
#         qs = Post.objects.all()
#         data = []
#         for obj in qs:
#             item = {
#                 'id': obj.id,
#                 'caption': obj.caption,
#                 'posted': obj.posted,
#                 'liked': True if request.user in obj.liked.all() else False,
#                 'user': obj.user.username,
#                 'count': obj.like_count,
#             }
#             data.append(item)
#         return JsonResponse({'data': data})


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


@login_required
def PostDetails(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    #profile = Profile.objects.get(user=request.user)
    favorited = False

    #Comment
    # comments = Comment.objects.filter(post=post).order_by('date')

    #Comment Form
    # if request.method == 'POST':
    #     form = CommentForm(request.POST)
    #     if form.is_valid():
    #         comment = form.save(commit=False)
    #         comment.post = post
    #         comment.user = request.user
    #         comment.save()
    #         return HttpResponseRedirect(reverse('postdetails', args=[post_id]))
    # else:
    #     form = CommentForm()

    #Favorite Color conditional
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)

        #For the color of the favorite button
        if profile.favorites.filter(id=post_id).exists():
            favorited = True

    template = loader.get_template('posts/posts_detail.html')

    context = {
        'post': post,
        'favorited': favorited,
        # 'form': form,
        # 'comments': comments,
    }
    return HttpResponse(template.render(context, request))


def post_detail_json(request, pk):
    obj = Post.objects.get(pk=pk)
    data = {
        'id': obj.id,
        'caption': obj.caption,
        'posted': obj.posted,
        'user': obj.user.username,
        'logged_in': request.user.username,
    }
    return JsonResponse({'data': data})


def update_posts(request, pk):
    obj = Post.objects.get(pk=pk)
    if request.is_ajax():
        new_caption = request.POST.get('caption')
        obj.caption = new_caption
        obj.save()
        return JsonResponse({
            'id': obj.id,
            'caption': obj.caption,
        })


def delete_posts(request, pk):
    obj = Post.objects.get(pk=pk)
    if request.is_ajax():
        obj.delete()
        return JsonResponse({})


@login_required
def tags(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    posts = Post.objects.filter(tags=tag).order_by('-posted')

    template = loader.get_template('tag.html')
    context = {
        'posts': posts,
        'tag': tag,
    }
    return HttpResponse(template.render(context,request))        


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
