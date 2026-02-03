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
import random

# Create test client
client = Client()

# Generate unique username
import time
unique_id = int(time.time() * 1000) % 10000
username = f'testuser{unique_id}'

# 1. Create user
try:
    user = User.objects.create_user(
        username=username,
        password='testpass123'
    )
    print(f"Created new user: {username}")
except:
    # Get existing user
    user = User.objects.filter(username__startswith='testuser').first()
    print(f"Using existing user: {user.username}")

# 2. Create category and location
category, created = Category.objects.get_or_create(
    slug='test-category-debug',
    defaults={
        'title': 'Test Category Debug',
        'is_published': True
    }
)

location, created = Location.objects.get_or_create(
    name='Test Location Debug',
    defaults={
        'is_published': True
    }
)

# 3. Create post
post = Post.objects.create(
    title=f'Test Post {unique_id}',
    text='Test content for debugging edit form',
    author=user,
    category=category,
    location=location,
    is_published=True,
    pub_date=timezone.now()
)

# 4. Create comment
comment = Comment.objects.create(
    text='Test comment text for editing - debug version',
    author=user,
    post=post
)

print("=== TEST DATA CREATED ===")
print(f"User: {user.username}")
print(f"Post: {post.title} (ID: {post.id})")
print(f"Comment ID: {comment.id}")

# 5. Login
client.login(username=user.username, password='testpass123')

# 6. Test edit page
print("\n=== TESTING EDIT PAGE ===")
edit_url = f'/posts/{post.id}/edit_comment/{comment.id}/'
print(f"URL: {edit_url}")

response = client.get(edit_url)
print(f"Status: {response.status_code}")

# 7. Check context
print("\n=== CHECKING CONTEXT ===")
if hasattr(response, 'context'):
    print("Context keys found:")
    for key in response.context.keys():
        print(f"  - {key}")
        
    if 'editing_comment' in response.context:
        ec = response.context['editing_comment']
        print(f"  editing_comment ID: {ec.id}")
        print(f"  Matches our comment: {ec.id == comment.id}")
    
    if 'comment_form' in response.context:
        form = response.context['comment_form']
        print(f"  Form found: {form.__class__.__name__}")
        print(f"  Form fields: {list(form.fields.keys())}")
        if hasattr(form, 'instance') and form.instance:
            print(f"  Form instance ID: {form.instance.id}")
            print(f"  Form initial text: '{form.initial.get('text', '')[:50]}...'")
    else:
        print("  ERROR: comment_form NOT in context!")
else:
    print("No context in response!")

# 8. Check HTML
print("\n=== CHECKING HTML ===")
html = response.content.decode('utf-8')

# Look for key elements
checks = [
    ('<form', 'Form tag'),
    ('method="post"', 'POST method'),
    ('csrf_token', 'CSRF token'),
    ('comment_form', 'Form variable'),
    ('Test comment text', 'Comment text in form'),
]

for text, desc in checks:
    found = text in html
    print(f"{'OK' if found else 'NO'} {desc}: {'Found' if found else 'Not found'}")

# 9. Count forms
import re
form_tags = re.findall(r'<form[^>]*>', html)
print(f"\nForm tags found: {len(form_tags)}")

if not form_tags:
    print("\n=== DEBUG: SHOWING HTML ===")
    print("First 1500 characters of HTML:")
    print(html[:1500])

print("\n=== TEST COMPLETE ===")
