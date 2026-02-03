# -*- coding: utf-8 -*-
import os
import re
import sys

import django
from blog.models import Comment, Post
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.test import Client

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blogicum.settings')
sys.path.insert(0, '/c/Dev/django_sprint4/blogicum')

django.setup()


User = get_user_model()

print("=== Тест отображения комментариев ===")

# 1. Создаем тестового пользователя
user, created = User.objects.get_or_create(
    username='testuser_debug',
    defaults={'password': 'testpass123'}
)
if created:
    user.set_password('testpass123')
    user.save()

# 2. Берем первый пост или создаем новый
post = Post.objects.first()
if not post:
    print("Создаем тестовый пост...")
    from blog.models import Category, Location
    category = Category.objects.first() or Category.objects.create(
        title='Test Category',
        slug='test-category',
        is_published=True
    )
    location = Location.objects.first() or Location.objects.create(
        name='Test Location',
        is_published=True
    )
    post = Post.objects.create(
        title='Тестовый пост для отладки',
        text='Содержание тестового поста',
        author=user,
        category=category,
        location=location,
        is_published=True
    )

# 3. Удаляем старые комментарии и создаем 3 новых
post.comments.all().delete()  # type: ignore
for i in range(3):
    Comment.objects.create(
        post=post,
        author=user,
        text=f'Тестовый комментарий {i+1}'
    )

print(f"Пост: {post.title}")
print(f"Комментариев у поста: {post.comments.count()}")  # type: ignore
print(f"Ожидаемый вывод: ({post.comments.count()})")  # type: ignore

# 4. Проверяем главную страницу
client = Client()
response = client.get('/')
content = response.content.decode('utf-8')

# 5. Ищем пост на странице
if post.title in content:
    print(f"\n✓ Пост '{post.title}' найден на главной")

    # Ищем все (число) на странице
    matches = re.findall(r'\((\d+)\)', content)
    print(f"Все числа в скобках на главной: {matches}")

    # Ищем конкретно наш пост
    pos = content.find(post.title)
    if pos != -1:
        # Берем фрагмент вокруг поста
        start = max(0, pos - 500)
        end = min(len(content), pos + 1000)
        fragment = content[start:end]

        # Ищем 'Комментарии' в этом фрагменте
        if 'Комментарии' in fragment:
            print("✓ Найдено 'Комментарии' возле поста")
            idx = fragment.find('Комментарии')
            # Покажем 150 символов после 'Комментарии'
            context = fragment[idx:idx + 150]
            print(f"Контекст: {context}")

            # Ищем (число) в этом контексте
            context_matches = re.findall(r'\((\d+)\)', context)
            print(f"Числа в скобках в контексте: {context_matches}")
        else:
            print("✗ 'Комментарии' не найдено возле поста")

            # Проверим что вообще есть в фрагменте
            print("\nЧто есть в фрагменте (первые 800 символов):")
            print(fragment[:800])
else:
    print(f"\n✗ Пост '{post.title}' НЕ найден на главной!")

# 6. Проверка profile страницы
print("\n=== Проверка profile страницы ===")
response = client.get(f'/profile/{user.username}/')  # type: ignore
content = response.content.decode('utf-8')
matches = re.findall(r'\((\d+)\)', content)
print(f"Числа в скобках на profile: {matches}")

# 7. Проверка прямого рендеринга шаблона
print("\n=== Прямой рендеринг шаблона ===")

# Рендерим post_card.html
try:
    rendered = render_to_string('includes/post_card.html', {'post': post})
    print("Успешно отрендерен шаблон")

    # Ищем (число) в отрендеренном шаблоне
    template_matches = re.findall(r'\((\d+)\)', rendered)
    print(f"Числа в скобках в отрендеренном шаблоне: {template_matches}")

    if 'Комментарии' in rendered:
        idx = rendered.find('Комментарии')
        print(f"Контекст из шаблона: {rendered[idx:idx+100]}")
    else:
        print("'Комментарии' не найдено в отрендеренном шаблоне!")

except Exception as e:
    print(f"Ошибка рендеринга: {e}")

print("\n=== Итог ===")
# type: ignore
count = post.comments.count()  # type: ignore
print(f"В шаблоне должно быть: 'Комментарии ({count})'")
print(f"На главной найдено чисел в скобках: {len(matches)}")
print("Ожидаем найти хотя бы одно: (3)")
