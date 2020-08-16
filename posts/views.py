from django.shortcuts import render, get_object_or_404
from .models import Post, Group
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

def index(request):
    latest = Post.objects.all()[:11]
    return render(request, "index.html", {"posts": latest})


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()[:12]
    context = {
        "group": group,
        "posts": posts
    }
    return render(request, "group.html", context)

@login_required
def new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            created_post = Post.objects.create(text=text, author = request.user) 
            created_post.save()
            return redirect('/index/')
        return render(request, 'index.html', {'form': form})
    form = PostForm()
    return render(request, 'new.html', {'form': form})

