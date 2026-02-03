from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView

from .forms import CommentForm, CreationForm, PostForm
from .models import Category, Comment, Post


def get_published_posts():
    return Post.objects.filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=timezone.now()
    ).select_related('category', 'location', 'author')


def index(request):
    post_list = get_published_posts().order_by('-pub_date')

    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/index.html', {
        'page_obj': page_obj,
        'title': 'Blog posts'
    })


def post_detail(request, id):
    # Получаем пост любым способом
    post = get_object_or_404(Post, pk=id)

    # Проверяем права доступа
    if (not post.is_published or post.pub_date
            > timezone.now() or not post.category.is_published):
        # Если пост не опубликован или отложен
        if request.user != post.author:
            # Не автору показываем 404
            raise Http404("Пост не найден")

    comments = post.comments.all()
    comment_form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'blog/detail.html', context)


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )

    post_list = get_published_posts().filter(
        category=category).order_by('-pub_date')

    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/category.html', {
        'category': category,
        'page_obj': page_obj
    })


# ========== ВРЕМЕННЫЕ ФУНКЦИИ ДЛЯ ТЕСТОВ ==========
def profile(request, username):
    """Перенаправление на users:profile для тестов"""
    return redirect('users:profile', username=username)


@login_required
def edit_profile(request):
    """Перенаправление на users:edit_profile для тестов"""
    return redirect('users:edit_profile', username=request.user.username)
# ================================================


@csrf_exempt  # ДОБАВЬТЕ ЭТУ СТРОКУ
@login_required
def post_create(request):
    print()
    print("=" * 50)
    print("DEBUG: post_create ВЫЗВАНА!")
    user = (request.user.username
            if request.user.is_authenticated
            else 'Anonymous')
    print(f"User: {user}")
    print(f"Method: {request.method}")
    print(f"Path: {request.path}")
    print(f"Full path: {request.get_full_path()}")
    print("=" * 50)

    if request.method == 'POST':
        print(f"POST data keys: {list(request.POST.keys())}")
        print(f"POST data values: {dict(request.POST)}")
        print(f"FILES: {dict(request.FILES)}")

        form = PostForm(request.POST, request.FILES)
        print(f"Form is bound: {form.is_bound}")

        if form.is_valid():
            print("✓ Форма ВАЛИДНА!")
            print(f"Cleaned data: {form.cleaned_data}")

            posts_before = Post.objects.count()
            print(f"Постов в базе до: {posts_before}")

            post = form.save(commit=False)
            post.author = request.user
            post.save()

            posts_after = Post.objects.count()
            print(f"Постов в базе после: {posts_after}")
            print(f"Создан пост: ID={post.id}, '{post.title}'")

            return redirect('users:profile', username=request.user.username)
        else:
            print("✗ Форма НЕВАЛИДНА!")
            print(f"Ошибки: {form.errors}")
    else:
        form = PostForm()
        print("GET запрос - показываем форму")

    return render(request, 'blog/create.html', {'form': form})


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.user != post.author:
        return redirect('blog:post_detail', id=post_id)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', id=post_id)
    else:
        form = PostForm(instance=post)

    return render(request, 'blog/create.html', {'form': form, 'post': post})


@login_required
def post_delete(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.user != post.author:
        return redirect('blog:post_detail', id=post_id)

    if request.method == 'POST':
        post.delete()
        # ИСПРАВЛЕНО: используем 'users:profile'
        return redirect('users:profile', username=request.user.username)

    # GET запрос - показываем подтверждение
    return render(request, 'blog/detail.html', {
        'post': post,
        'confirm_delete': True
    })


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()

    return redirect('blog:post_detail', id=post_id)


@login_required
def edit_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id, post_id=post_id)

    if request.user != comment.author:
        return redirect('blog:post_detail', id=post_id)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', id=post_id)
    else:
        form = CommentForm(instance=comment)

    # ИСПРАВЬТЕ: используйте правильный шаблон!
    return render(request, 'blog/comment.html', {
        'form': form,  # Форма ДОЛЖНА быть здесь
        'post': comment.post,
        'comment': comment,
        'editing_comment': True  # флаг для шаблона (True, а не comment!)
    })


@login_required
def delete_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id, post_id=post_id)

    if request.user != comment.author:
        return redirect('blog:post_detail', id=post_id)

    if request.method == 'POST':
        comment.delete()
        return redirect('blog:post_detail', id=post_id)

    # ВАЖНО: НЕ ПЕРЕДАВАТЬ comment_form!
    # Только минимальный контекст
    return render(request, 'blog/detail.html', {
        'post': comment.post,
        'comment': comment,
        'confirm_delete_comment': True  # только этот флаг
    })


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('blog:index')
    template_name = 'registration/registration.html'
