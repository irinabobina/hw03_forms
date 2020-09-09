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

@login_required
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
 
 
#def post_view(request, username, post_id):
        # тут тело функции
        #return render(request, 'post.html', {})


#def post_edit(request, username, post_id):
        # тут тело функции. Не забудьте проверить, 
        # что текущий пользователь — это автор записи.
        # В качестве шаблона страницы редактирования укажите шаблон создания новой записи
        # который вы создали раньше (вы могли назвать шаблон иначе)
        #return render(request, 'post_new.html', {})
