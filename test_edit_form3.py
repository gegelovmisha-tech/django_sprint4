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

# Create test client
client = Client()

# Generate unique username
unique_id = int(time.time() * 1000) % 10000
username = f'testuser{unique_id}'

print(f"=== STARTING TEST FOR USER: {username} ===")

# 1. Create user
try:
    user = User.objects.create_user(
        username=username,
        password='testpass123'
    )
    print(f"Created new user: {username}")
except Exception as e:
    print(f"Error creating user: {e}")
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

print(f"Created: Post ID={post.id}, Comment ID={comment.id}")

# 5. Login
login_result = client.login(username=user.username, password='testpass123')
print(f"Login result: {login_result}")

# 6. Test edit page
print("\n=== TESTING EDIT PAGE ===")
edit_url = f'/posts/{post.id}/edit_comment/{comment.id}/'
print(f"URL: {edit_url}")

response = client.get(edit_url)
print(f"Status: {response.status_code}")
print(f"Response type: {type(response)}")
print(f"Has context: {hasattr(response, 'context')}")

# Check if it's a TemplateResponse
from django.template.response import TemplateResponse
if isinstance(response, TemplateResponse):
    print("Response is TemplateResponse")
    # Force rendering
    response.render()
    print("Response rendered")

# 7. Check context - SAFER WAY
print("\n=== CHECKING CONTEXT ===")
try:
    if hasattr(response, 'context'):
        print(f"Context is not None: {response.context is not None}")
        if response.context:
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
            else:
                print("  ERROR: comment_form NOT in context!")
        else:
            print("Context exists but is empty/None")
    else:
        print("Response has no 'context' attribute")
        
except Exception as e:
    print(f"Error checking context: {e}")

# 8. Check HTML anyway
print("\n=== CHECKING HTML CONTENT ===")
html = response.content.decode('utf-8')
print(f"HTML length: {len(html)} characters")

# Basic checks
checks = [
    ('<form', 'Form tag'),
    ('method="post"', 'POST method'),
    ('csrf_token', 'CSRF token'),
    ('comment_form', 'Form variable'),
    ('Test comment text', 'Comment text'),
    ('editing_comment', 'Editing comment variable'),
]

for text, desc in checks:
    found = text in html
    print(f"{'' if found else ''} {desc}: {'Found' if found else 'Not found'}")

# 9. Show HTML snippet for debugging
print("\n=== HTML SNIPPET (first 1000 chars) ===")
print(html[:1000])

# 10. Look for form specifically
import re
form_tags = re.findall(r'<form[^>]*>', html)
print(f"\nForm tags found in HTML: {len(form_tags)}")

if form_tags:
    for i, tag in enumerate(form_tags, 1):
        print(f"Form {i}: {tag[:100]}")
        
        # Check URL
        if 'edit_comment' in tag:
            print("  ^ This looks like edit comment form!")
else:
    print("NO FORM TAGS FOUND IN HTML!")

print("\n=== TEST COMPLETE ===")
