from django.shortcuts import render, redirect
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    posts = Post.objects.all()
    context = {
        'posts' : posts,
    }
    return render(request, 'posts/index.html', context)

def detail(request, post_pk):
     post = Post.objects.get(pk=post_pk)
     comments = post.comment_set.all()
     comment_form = CommentForm()

     context = {
          'post' : post,
          'comments' : comments,
          'comment_form' : comment_form,
     }
     return render(request, 'posts/detail.html', context)

@login_required
def create(request):
    if request.method == 'POST': # POST면 create
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('posts:detail', post.pk)
    else: # GET이면 new
            form = PostForm()
        
    context = {
        'form' : form,
    }
    return render(request, 'posts/create.html', context)

@login_required
def update(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    if request.method == 'POST': # POST면 update
        form = PostForm(request.POST, instance=post) # 인스턴스로 수정임을 표시 
        if form.is_valid():
            form.save()
            return redirect('posts:detail', post.pk)
    else: # GET이면 edit
        form = PostForm(instance=post)
		
    context = {
        'post' : post,
        'form' : form,
    }
    return render(request, 'posts/update.html', context)

@login_required
def delete(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    post.delete()
    return redirect('posts:index')

@login_required
def comments_create(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    comment_form = CommentForm(request.POST)

    if comment_form.is_valid():
        comment = comment_form.save(commit=False) # commit False는 DB에 저장 요청을 보류하고, comment 인스턴스는 반환
        comment.user = request.user
        comment.post = post
        comment.save()
        return redirect('posts:detail', post.pk)
    context = {
        'post' : post,
        'comment_form' : comment_form,
    }
    return render(request, 'posts/detail.html', context)

@login_required
def comments_delete(request, post_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if request.user == comment.user:
        comment.delete()

    return redirect('posts:detail', post_pk)
