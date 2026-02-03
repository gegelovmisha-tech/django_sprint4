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
from django.http import HttpResponse

# Create test data
user = User.objects.create_user('debuguser', 'debug@test.com', 'debugpass')
category = Category.objects.create(title='Debug', slug='debug', is_published=True)
location = Location.objects.create(name='Debug', is_published=True)

post = Post.objects.create(
    title='Debug Post',
    text='Debug content',
    author=user,
    category=category,
    location=location,
    is_published=True,
    pub_date=timezone.now()
)

comment = Comment.objects.create(
    text='Debug comment for editing',
    author=user,
    post=post
)

print(f"Post ID: {post.id}, Comment ID: {comment.id}")

# Call function directly
factory = RequestFactory()
request = factory.get(f'/posts/{post.id}/edit_comment/{comment.id}/')
request.user = user

print("\n=== DIRECT FUNCTION CALL ===")
response = edit_comment(request, post.id, comment.id)

print(f"Response type: {type(response)}")
print(f"Is HttpResponse: {isinstance(response, HttpResponse)}")
print(f"Status code: {response.status_code}")

# Check if it's a TemplateResponse
from django.template.response import TemplateResponse
if isinstance(response, TemplateResponse):
    print("Is TemplateResponse: YES")
    print(f"Template name: {response.template_name}")
    
    # Force rendering
    print("Rendering response...")
    response.render()
    
    print(f"Has context: {hasattr(response, 'context')}")
    if hasattr(response, 'context'):
        print(f"Context keys: {list(response.context.keys()) if response.context else 'Empty'}")
        
        if response.context and 'comment_form' in response.context:
            print("SUCCESS: comment_form in context!")
            form = response.context['comment_form']
            print(f"  Form type: {form.__class__.__name__}")
            print(f"  Instance ID: {form.instance.id if hasattr(form, 'instance') else 'No instance'}")
else:
    print("Is TemplateResponse: NO")
    
# Check content
print("\n=== CHECKING CONTENT ===")
content = response.content.decode('utf-8') if hasattr(response, 'content') else 'No content'
print(f"Content length: {len(content)}")

# Basic checks
if '<form' in content:
    print(" Form tag found in content")
else:
    print(" Form tag NOT found in content")
    print("First 500 chars of content:")
    print(content[:500])
