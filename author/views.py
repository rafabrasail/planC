from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash

from author.models import Profile
from author.forms import SignUpForm, ChangePasswordForm, EditProfileForm
from django.db import transaction
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect

from django.core.paginator import Paginator
from django.urls import resolve, reverse


def UserMainPage(request, username):
    user = get_object_or_404(User, username=username)
    # profile = Profile.objects.get(user=user)
    url_name = resolve(request.path).url_name
	
    # if url_name == 'profile':
    #     posts = Post.objects.filter(user=user).order_by('-posted')
    # else:
    #     posts = profile.favorites.all()

    #Profile info box
    # posts_count = Post.objects.filter(user=user).count()
    # following_count = Follow.objects.filter(follower=user).count()
    # followers_count = Follow.objects.filter(following=user).count()

	#follow status
    # follow_status = Follow.objects.filter(following=user, follower=request.user).exists()

    #Pagination
    # paginator = Paginator(posts, 8)
    # page_number = request.GET.get('page')
    # posts_paginator = paginator.get_page(page_number)

    template = loader.get_template('mainpage.html')

    context = {
        # 'profile':profile,
        # 'posts': posts_paginator,
        # 'following_count':following_count,
        # 'followers_count':followers_count,
        # 'posts_count':posts_count,
        # 'follow_status':follow_status,
        'url_name':url_name,
    }

    return HttpResponse(template.render(context, request))


def SignUp(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            User.objects.create_user(username=username, email=email, password=password)
            return redirect('login')
    else:
        form = SignUpForm()

    context = {
        'form': form
    }

    return render(request, 'author/signup.html', context)