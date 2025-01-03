from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
# Create your views here.
def index(request):
    posts = Post.objects.all()
    return render(request, "blog/index.html", context={
        'posts': posts,
    })

def blogpost(request, id):
    try: post = get_object_or_404(Post, id=id)
    except: return redirect("index")
    return render(request, "blog/blogpost.html", context={
        "post": post
    })

def about(request):
    return render(request, "blog/about.html", context=None)