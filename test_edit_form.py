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

# Create test client
client = Client()

# 1. Create user
user = User.objects.create_user(
    username='testuser',
    password='testpass123'
)

# 2. Create category and location
category = Category.objects.create(
    title='Test Category',
    slug='test-category',
    is_published=True
)

location = Location.objects.create(
    name='Test Location',
    is_published=True
)

# 3. Create post
post = Post.objects.create(
    title='Test Post',
    text='Test content',
    author=user,
    category=category,
    location=location,
    is_published=True,
    pub_date=timezone.now()
)

# 4. Create comment
comment = Comment.objects.create(
    text='Test comment text for editing',
    author=user,
    post=post
)

print("=== TEST DATA CREATED ===")
print(f"User: {user.username}")
print(f"Post: {post.title} (ID: {post.id})")
print(f"Comment ID: {comment.id}")

# 5. Login
client.login(username='testuser', password='testpass123')

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
    
    if 'comment_form' in response.context:
        form = response.context['comment_form']
        print(f"  Form found: {form.__class__.__name__}")
        print(f"  Form fields: {list(form.fields.keys())}")
        if hasattr(form, 'instance') and form.instance:
            print(f"  Form instance ID: {form.instance.id}")
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

# 9. Check form specifically
print("\n=== LOOKING FOR FORM ===")
import re

form_tags = re.findall(r'<form[^>]*>', html)
print(f"Form tags found: {len(form_tags)}")

if form_tags:
    for i, tag in enumerate(form_tags, 1):
        print(f"Form {i}: {tag[:80]}")
        
        # Check if it's edit comment form
        if 'edit_comment' in tag:
            print("  ^ This is edit comment form!")
else:
    print("NO FORM TAGS FOUND!")
    
    # Debug: show HTML snippet
    print("\nHTML snippet (first 1000 chars):")
    print(html[:1000])

print("\n=== TEST COMPLETE ===")
