from email.mime import image
import re
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Post
from django.utils import timezone
from django.contrib.auth.decorators import login_required
import requests


# Create your views here.
def index(request):
    dog_api_response = requests.get('https://dog.ceo/api/breeds/image/random')
    dog_api_response_dictionary = dog_api_response.json()
    dog = None
    if dog_api_response_dictionary.get('status') == 'success':
        dog = dog_api_response_dictionary.get('message')

    posts = Post.objects.all()
    context = {'posts': posts, 'dog': dog}

    return render(request, 'posts/index.html', context)


def detail(request, post_id):
    post = Post.objects.get(id=post_id)
    context = { 'post' : post }

    return render(request, 'posts/detail.html', context)

@login_required
def new(request):
    return render(request, 'posts/new.html')

@login_required
def create(request):

    user = request.user
    body = request.POST.get('body')
    image = request.FILES.get('image')

    post = Post(user=user, body=body, image=image, created_at=timezone.now())
    post.save()

    return redirect('posts:detail', post_id=post.id)

@login_required
def edit(request, post_id):
    try:
        post = Post.objects.get(id=post_id, user=request.user)
    except Post.DoesNotExist:
        return redirect('posts:index')

    context = { 'post' : post }

    return render(request, 'posts/edit.html', context)

@login_required
def update(request, post_id):
    try:
        post = Post.objects.get(id=post_id, user=request.user)
    except Post.DoesNotExist:
        return redirect('posts:index')

    post.body = request.POST.get('body')
    image = request.FILES.get('image')
    if image:
        post.image = image 

    post.save()

    return redirect('posts:detail', post_id=post.id)

@login_required
def delete(request, post_id):
    try:
        post = Post.objects.get(id=post_id, user=request.user)
    except Post.DoesNotExist:
        return redirect('posts:index')

    post.delete()
    
    return redirect('posts:index')

@login_required
def like(request, post_id):
	if request.method == 'POST': 
		try:
		    post = Post.objects.get(id=post_id)

		    if request.user in post.liked_users.all():
		        post.liked_users.remove(request.user)
		    else:
		        post.liked_users.add(request.user)
	        
		    return redirect('posts:detail', post_id=post.id)
    
		except Post.DoesNotExist:
		    pass

	return redirect('posts:index')