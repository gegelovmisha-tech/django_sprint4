import os
import sys
sys.path.append('blogicum')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blogicum.settings')

import django
django.setup()

from blog.views import edit_comment
from django.test import RequestFactory
from django.contrib.auth.models import User
from blog.models import Post, Comment, Category, Location
from django.utils import timezone

# Create data
user = User.objects.create_user('checkuser', 'check@test.com', 'checkpass')
category = Category.objects.create(title='Check', slug='check', is_published=True)
location = Location.objects.create(name='Check', is_published=True)

post = Post.objects.create(
    title='Check Post',
    text='Check',
    author=user,
    category=category,
    location=location,
    is_published=True,
    pub_date=timezone.now()
)

comment = Comment.objects.create(
    text='Check comment',
    author=user,
    post=post
)

print(f"Post ID: {post.id}, Comment ID: {comment.id}")

# Test the function directly
factory = RequestFactory()
request = factory.get(f'/posts/{post.id}/edit_comment/{comment.id}/')
request.user = user

print("\n=== CALLING edit_comment FUNCTION ===")
try:
    response = edit_comment(request, post.id, comment.id)
    print(f"Response type: {type(response)}")
    print(f"Response status: {response.status_code}")
    
    # Check what's returned
    if hasattr(response, 'context_data'):
        print(f"Has context_data: {response.context_data}")
    if hasattr(response, 'context'):
        print(f"Has context: {response.context}")
        
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()

print("\n=== CHECKING URL PATTERN ===")
# Check URL pattern
from django.urls import resolve, Resolver404
try:
    match = resolve(f'/posts/{post.id}/edit_comment/{comment.id}/')
    print(f"URL resolves to: {match.view_name}")
    print(f"View function: {match.func}")
    print(f"URL args: {match.args}, kwargs: {match.kwargs}")
except Resolver404:
    print("URL does not resolve!")
except Exception as e:
    print(f"Error resolving URL: {e}")
