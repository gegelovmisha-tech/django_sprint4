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
import time

# Generate unique data
unique_id = int(time.time() * 1000) % 10000
username = f'ctxuser{unique_id}'

user = User.objects.create_user(username, f'{username}@test.com', 'testpass')
category = Category.objects.create(title='CtxCat', slug=f'ctxcat-{unique_id}', is_published=True)
location = Location.objects.create(name='CtxLoc', is_published=True)

post = Post.objects.create(
    title=f'Ctx Post {unique_id}',
    text='Context test',
    author=user,
    category=category,
    location=location,
    is_published=True,
    pub_date=timezone.now()
)

comment = Comment.objects.create(
    text='Context test comment',
    author=user,
    post=post
)

print(f"Created: Post ID={post.id}, Comment ID={comment.id}")

# Call function directly
factory = RequestFactory()
request = factory.get(f'/posts/{post.id}/edit_comment/{comment.id}/')
request.user = user

print("\n=== CALLING EDIT_COMMENT ===")
response = edit_comment(request, post.id, comment.id)

print(f"Response type: {type(response)}")

# Check what's in the response
if hasattr(response, 'context_data'):
    print(f"context_data: {response.context_data}")
elif hasattr(response, 'context'):
    print(f"context type: {type(response.context)}")
    
    # Try to force render
    try:
        from django.template.response import TemplateResponse
        if isinstance(response, TemplateResponse):
            print("Is TemplateResponse, rendering...")
            response.render()
            print(f"After render, context: {response.context}")
            
            if response.context:
                print("\n=== CONTEXT CONTENTS ===")
                for key, value in response.context.items():
                    print(f"{key}: {type(value).__name__}")
                    
                    if key == 'comments':
                        print(f"  Length: {len(value) if hasattr(value, '__len__') else 'N/A'}")
                        if hasattr(value, '__len__') and len(value) > 0:
                            for i, c in enumerate(value[:3], 1):
                                print(f"  Comment {i}: ID={c.id}, text='{c.text[:30]}...'")
                    elif key == 'editing_comment':
                        print(f"  ID: {value.id}, text='{value.text[:30]}...'")
            else:
                print("Context is empty!")
    except Exception as e:
        print(f"Error: {e}")
