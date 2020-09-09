from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.core.paginator import Paginator

from .models import Post, Group
from .forms import PostForm


def index(request):
    latest = Post.objects.all()[:11]
    paginator = Paginator(latest, 10)  # показывать по 10 записей на странице.

    page_number = request.GET.get('page')  # переменная в URL с номером запрошенной страницы
    page = paginator.get_page(page_number)  # получить записи с нужным смещением
    return render(
        request,
        'index.html',
        {'page': page, 'posts': latest, 'paginator': paginator}
       )

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
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.instance.author = request.user
            form.save()
            return redirect('index')
        return render(request, 'index.html', {'form': form}) 
    return render(request, 'new.html', {'form': form})

def profile(request, username):
    profile = get_object_or_404(get_user_model(), username=username)
    post_list = profile.posts.order_by('-pub_date').all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'profile': profile,
        'page': page,
        'paginator': paginator,
        'post_list': post_list
    }
    return render(request, 'profile.html', context)
 
 
def post_view(request, username, post_id):
        author = get_object_or_404(get_user_model(), username=username)
        count_post = Post.objects.order_by('-pub_date').filter(author=author).all().count()
        view_post = get_object_or_404(post, id=post_id)
        context = {
            'profile': author,
            'post': view_post,
            'count_post': count_post
        }
        return render(request, 'post.html', context)

@login_required
def post_edit(request, username, post_id):
    context = {
        'page_name': 'Редактирование поста',
        'button_name': 'Сохранить',
    }

    if request.user.username == username:
        edit_post = get_object_or_404(Post, id=post_id)
        form = PostForm(instance=edit_post)
        if request.method == "POST":
            if form.is_valid():
                form = PostForm(request.POST, instance=edit_post)
                form.save()
                return redirect('index')
            context['form'] = form
            return render(request, 'new.html', context)
        context['form'] = form
        return render(request, 'new.html', context)