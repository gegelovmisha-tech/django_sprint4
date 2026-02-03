import os

import django
from blog.models import Category, Location, Post
from django.contrib.auth import get_user_model
from django.test import Client

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blogicum.settings')
django.setup()


User = get_user_model()

print("=== ТЕСТ: Комментарий к удаленному посту ===")

# 1. Находим любого пользователя
user = User.objects.first()
if not user:
    print("Нет пользователей в базе!")
    exit(1)

print(f"Пользователь: {user.username}")  # type: ignore

# 2. Создаем пост если нет
post = Post.objects.first()
if not post:
    print("Создаем тестовый пост...")
    category = Category.objects.first() or Category.objects.create(
        title='Test', slug='test', is_published=True
    )
    location = Location.objects.first() or Location.objects.create(
        name='Test', is_published=True
    )
    post = Post.objects.create(
        title='Test Post',
        text='Content',
        pub_date='2025-01-01 00:00:00',
        author=user,
        category=category,
        is_published=True
    )

print(f"Пост ID: {post.id}, заголовок: '{post.title}'")  # type: ignore

# 3. Тестируем
client = Client()
client.force_login(user)

# Тест 1: Комментарий к существующему посту
print("\n1. POST к существующему посту:")
response = client.post(
    f'/posts/{post.id}/comment/', {'text': 'Test'})  # type: ignore
print(f"   Статус: {response.status_code}")
print(f"   Редирект: {response.url if hasattr(response, 'url') else 'Нет'}")

# Тест 2: Комментарий к удаленному посту
print("\n2. Удаляем пост...")
post_id = post.id  # type: ignore
post.delete()

print(f"   POST к удаленному посту (ID: {post_id}):")
try:
    response = client.post(f'/posts/{post_id}/comment/', {'text': 'Test'})
    print(f"   Статус: {response.status_code}")
    if response.status_code == 404:
        print("   ✓ Вернул 404 (правильно)")
    else:
        print(f"   ⚠️ Вернул {response.status_code} (ожидалось 404)")
except Exception as e:
    print(f"   Исключение: {type(e).__name__}: {e}")

print("\n=== ТЕСТ ЗАВЕРШЕН ===")
