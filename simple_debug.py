import os
import sys
sys.path.append('blogicum')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blogicum.settings')

import django
django.setup()

from blog.models import Post, Comment, Category, Location
from django.contrib.auth.models import User
from blog.views import edit_comment
from django.test import RequestFactory
from django.utils import timezone

# Создаем пользователя
user = User.objects.create_user('debuguser', 'debug@test.com', 'debugpass')

# Создаем пост
category = Category.objects.create(title='Debug', slug='debug', is_published=True)
location = Location.objects.create(name='Debug', is_published=True)
post = Post.objects.create(
    title='Debug Post',
    text='Debug',
    author=user,
    category=category,
    location=location,
    is_published=True,
    pub_date=timezone.now()
)

# Создаем 2 комментария
comment1 = Comment.objects.create(text='Comment 1', author=user, post=post)
comment2 = Comment.objects.create(text='Comment 2', author=user, post=post)

print(f"Comment1 ID: {comment1.id}")
print(f"Comment2 ID: {comment2.id}")

# Тестируем редактирование comment1
factory = RequestFactory()
request = factory.get(f'/posts/{post.id}/edit_comment/{comment1.id}/')
request.user = user

response = edit_comment(request, post.id, comment1.id)

print(f"\nResponse status: {response.status_code}")
print(f"Context has 'editing_comment': {'editing_comment' in response.context}")
if 'editing_comment' in response.context:
    print(f"Editing comment ID in context: {response.context['editing_comment'].id}")

print(f"Context has 'comments': {'comments' in response.context}")
if 'comments' in response.context:
    print(f"Number of comments in context: {len(response.context['comments'])}")
    for c in response.context['comments']:
        print(f"  - Comment ID: {c.id}, Text: {c.text[:20]}...")

# Проверим HTML
html = response.content.decode('utf-8')
print(f"\nHas '<form' in HTML: {'<form' in html}")
print(f"Has 'Comment 1' in HTML: {'Comment 1' in html}")
print(f"Has 'Comment 2' in HTML: {'Comment 2' in html}")

# Поищем форму
import re
forms = re.findall(r'<form[^>]*>', html)
print(f"\nNumber of form tags found: {len(forms)}")
if forms:
    print("First form found:", forms[0][:100])
