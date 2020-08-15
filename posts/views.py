from django.shortcuts import render, get_object_or_404
from .models import Post, Group
from .forms import PostForm

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
            Post.group = form.cleaned_data['group'] 
            Post.text = form.cleaned_data['text']
            Post.save()
            return redirect('index')
    form = PostForm()
    return render(request, 'new.html', {'PostForm': form})