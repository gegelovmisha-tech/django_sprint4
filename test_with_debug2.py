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

# Generate unique username
unique_id = int(time.time() * 1000) % 10000
username = f'testuser{unique_id}'

# Get or create user
try:
    user = User.objects.create_user(username, f'{username}@test.com', 'testpass')
    print(f"Created user: {username}")
except:
    user = User.objects.filter(username__startswith='testuser').first()
    print(f"Using existing user: {user.username}")

category = Category.objects.create(title='DebugCat', slug=f'debugcat-{unique_id}', is_published=True)
location = Location.objects.create(name='DebugLoc', is_published=True)

post = Post.objects.create(
    title=f'Debug Post {unique_id}',
    text='Debug content',
    author=user,
    category=category,
    location=location,
    is_published=True,
    pub_date=timezone.now()
)

comment = Comment.objects.create(
    text='Debug comment for editing test',
    author=user,
    post=post
)

comment2 = Comment.objects.create(
    text='Second comment',
    author=user,
    post=post
)

print("=== TEST WITH DEBUG ===")
print(f"Post ID: {post.id}")
print(f"Comment 1 ID: {comment.id}")
print(f"Comment 2 ID: {comment2.id}")

client.login(username=user.username, password='testpass')
response = client.get(f'/posts/{post.id}/edit_comment/{comment.id}/')

html = response.content.decode('utf-8')

import re
debug_comments = re.findall(r'<!-- DEBUG:.*?-->', html)
print(f"\nFound {len(debug_comments)} debug comments:")
for i, dbg in enumerate(debug_comments, 1):
    print(f"{i}. {dbg}")

if '<form' in html:
    print("\n FORM FOUND")
    pos = html.find('<form')
    start = max(0, pos - 200)
    end = min(len(html), pos + 300)
    print("Form context:")
    print(html[start:end])
else:
    print("\n NO FORM FOUND")
    print("First 1000 chars of HTML:")
    print(html[:1000])
    
    # Check if debug comments exist
    if not debug_comments:
        print("\n NO DEBUG COMMENTS FOUND - template may not be rendered correctly")
