from blog.models import Post
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView

from .forms import CreationForm, EditProfileForm

User = get_user_model()


class SignUp(CreateView):
    """View for user registration."""

    form_class = CreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/registration_form.html'


def profile(request, username):
    """View for user profile page."""
    user = get_object_or_404(User, username=username)

    # Get all user posts
    posts_list = Post.objects.filter(author=user)

    # If not the author, show only published posts
    if request.user != user:
        posts_list = posts_list.filter(
            is_published=True,
            category__is_published=True,
            pub_date__lte=timezone.now()
        )

    # Статистика (БЕЗ дополнительных запросов к БД)
    total_posts = posts_list.count()
    published_posts = posts_list.filter(is_published=True).count()

    # Последний пост (уже есть в posts_list)
    last_post = posts_list.order_by('-pub_date').first()

    # Последний вход
    last_login = user.last_login

    # Sorting and pagination
    posts_list = posts_list.order_by('-pub_date')
    paginator = Paginator(posts_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'profile_user': user,
        'page_obj': page_obj,
        'total_posts': total_posts,
        'published_posts': published_posts,
        'last_post': last_post,
        'last_login': last_login,
    }
    return render(request, 'blog/profile.html', context)


@login_required
def edit_profile(request, username):
    """View for editing profile."""
    print("\n=== DEBUG edit_profile ===")
    print(f"User: {request.user.username}, Target: {username}")
    print(f"Method: {request.method}")

    # Разбиваем длинные строки
    if request.method == 'POST':
        post_keys = list(request.POST.keys())
    else:
        post_keys = 'No POST'
    print(f"POST keys: {post_keys}")

    if request.method == 'GET':
        get_keys = list(request.GET.keys())
    else:
        get_keys = 'No GET'
    print(f"GET keys: {get_keys}")

    user = get_object_or_404(User, username=username)

    if request.user != user:
        return redirect('users:profile', username=username)

    if request.method == 'POST':
        print(f"Full POST data: {dict(request.POST)}")
        form = EditProfileForm(request.POST, instance=user)
        if form.is_valid():
            print("Form valid! Saving...")
            form.save()
            return redirect('users:profile', username=username)
        else:
            print(f"Form INVALID! Errors: {form.errors}")
    else:
        form = EditProfileForm(instance=user)

    return render(request, 'users/edit_profile.html', {'form': form})
