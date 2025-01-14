from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import *
# Create your views here.
def index(request):
    posts = Post.objects.all().order_by('-created_at')[:20]
    return render(request, "blog/index.html", context={
        'posts': posts,
    })

def blogPost(request, id):
    try: post = get_object_or_404(Post, id=id)
    except: return redirect("index")
    if request.method == "POST":
        if not request.user.is_authenticated: return redirect("login")
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
    else:
        form = CommentForm() 
    comments = Comment.objects.filter(post=post).order_by('-created_at')[:100]
    return render(request, "blog/blogpost.html", context={
        "post": post,
        "comments": comments,
        "form": form,
    })

def editComment(request, id):
    try: comment = get_object_or_404(Comment, id=id)
    except: return redirect("index")
    if not request.user == comment.author: return redirect("index")
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.edited = True
            comment.save()
            return redirect("blogpost", id=comment.post.id)
    else:
        form = CommentForm(instance=comment)
    return render(request, "blog/editcomment.html", {
        "form": form
    })

def deleteComment(request, id):
    try: comment = get_object_or_404(Comment, id=id)
    except: redirect("index")
    post = comment.post
    if not request.user.is_superuser and not request.user == comment.author: redirect("index")
    comment.delete()
    return redirect("blogpost", id=post.id)

def about(request):
    return render(request, "blog/about.html", context=None)

def addPost(request):
    if request.method == "POST":
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save( commit=False )
            post.author = request.user
            post.save()
            return redirect("blogpost", id=post.id)
    else:
        form = AddPostForm()
    return render(request, "blog/addpost.html", {
        "form": form
    })

def editPost(request, id):
    try: post = get_object_or_404(Post, id=id)
    except: return redirect("index")
    if not request.user == post.author: return redirect("index")
    if request.method == "POST":
        form = AddPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            return redirect("blogpost", id=post.id)
    else:
        form = AddPostForm(instance=post)
    return render(request, "blog/editpost.html", {
        "form": form
    })

def deletePost(request, id):
    try: post = get_object_or_404(Post, id=id)
    except: redirect("index")
    if not request.user.is_superuser and not request.user == post.author: redirect("index")
    post.delete()
    return redirect("index")

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("index")
    else:
        form = RegisterForm()
    return render(request, "blog/register.html", {
        "form": form
    })

def userPage(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user).order_by('-created_at')

    return render(request, "blog/userpage.html", {
        "posts": posts,
        "user": user,
    })