from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash

from author.models import Profile
from author.forms import SignUpForm, ChangePasswordForm, EditProfileForm
from django.db import transaction
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect

from django.core.paginator import Paginator
from django.urls import resolve, reverse
from posts.models import Post, Follow
from users.models import User
#from django.contrib.auth.models import User
#from django.contrib.auth import get_user_model
#User = get_user_model()


@login_required
def UserMainPage(request, username):
    user = get_object_or_404(User, username=username)
    # user = get_object_or_404(settings.AUTH_USER_MODEL, username=username)
    profile = Profile.objects.get(user=user)
    url_name = resolve(request.path).url_name
	
    if url_name == 'profile':
        posts = Post.objects.filter(user=user).order_by('-posted')
    else:
        posts = profile.favorites.all()

    #Profile info box
    posts_count = Post.objects.filter(user=user).count()
    following_count = Follow.objects.filter(follower=user).count()
    followers_count = Follow.objects.filter(following=user).count()

	#follow status
    follow_status = Follow.objects.filter(following=user, follower=request.user).exists()

    #Pagination
    paginator = Paginator(posts, 8)
    page_number = request.GET.get('page')
    posts_paginator = paginator.get_page(page_number)

    template = loader.get_template('author/profile.html')

    context = {
        'profile':profile,
        'posts': posts_paginator,
        'following_count':following_count,
        'followers_count':followers_count,
        'posts_count':posts_count,
        'follow_status':follow_status,
        'url_name':url_name,
    }

    return HttpResponse(template.render(context, request))


def SignUp(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            # born = form.cleaned_data.get('born')
            password = form.cleaned_data.get('password')
            User.objects.create_user(
                first_name=first_name, 
                last_name=last_name, 
                # born=born,
                username=username, 
                email=email, 
                password=password)
            return redirect('login')
    else:
        form = SignUpForm()

    context = {
        'form': form
    }

    return render(request, 'author/signup.html', context)


def ContinueRegisterSingUp(request):
    if request.method == "POST":
        form = EditProfileForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            location = form.cleaned_data.get('location')
            url = form.cleaned_data.get('url')
            profile_info = form.cleaned_data.get('profile_info')
            born = form.cleaned_data.get('born')
            favorite_foot = form.cleaned_data.get('favorite_foot')
            club = form.cleaned_data.get('club')
            picture = form.cleaned_data.get('picture')
            settings.AUTH_USER_MODEL.objects.create_user(
                first_name=first_name, 
                last_name=last_name, 
                location = location,
                url=url,
                profile_info=profile_info,
                born = born, 
                favorite_foot=favorite_foot,
                club=club,
                picture=picture
                )
            return redirect('mainpage')
    else:
        form = EditProfileForm()

    context = {
        'form': form
    }

    return render(request, 'author/cont_profile.html', context)


def ChangePasswordByUser(request):
    user = request.user
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data.get('new_password')
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
            return redirect('')
    else:
        form = ChangePasswordForm(instance = user)

    context = {
        'form': form
    }

    return render(request, '', context)


