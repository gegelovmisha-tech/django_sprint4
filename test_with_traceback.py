import os
import sys
sys.path.append('blogicum')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blogicum.settings')

import django
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from blog.models import Post, Comment, Category, Location
from django.utils import timezone
import time

client = Client()
unique_id = int(time.time() * 1000) % 10000
username = f'traceuser{unique_id}'

user = User.objects.create_user(username, f'{username}@test.com', 'testpass')
category = Category.objects.create(title='Trace', slug=f'trace-{unique_id}', is_published=True)
location = Location.objects.create(name='Trace', is_published=True)

post = Post.objects.create(
    title=f'Trace Post {unique_id}',
    text='Trace test',
    author=user,
    category=category,
    location=location,
    is_published=True,
    pub_date=timezone.now()
)

comment = Comment.objects.create(
    text='Trace test comment',
    author=user,
    post=post
)

print(f"Created: Post ID={post.id}, Comment ID={comment.id}")

# Capture output
import io
from contextlib import redirect_stdout, redirect_stderr

f = io.StringIO()
with redirect_stdout(f), redirect_stderr(f):
    client.login(username=username, password='testpass')
    response = client.get(f'/posts/{post.id}/edit_comment/{comment.id}/')

output = f.getvalue()
print("\n=== CAPTURED OUTPUT ===")
print(output)

print(f"\nResponse status: {response.status_code}")
print(f"Is redirect: {response.status_code in [301, 302, 303, 307, 308]}")

if response.status_code == 200:
    html = response.content.decode('utf-8')
    print(f"HTML length: {len(html)}")
    print(f"Has form: {'<form' in html}")
