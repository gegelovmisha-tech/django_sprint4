import os
import sys
sys.path.append('blogicum')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blogicum.settings')

# Enable Django logging
import logging
logging.basicConfig(level=logging.DEBUG)

import django
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from blog.models import Post, Comment, Category, Location
from django.utils import timezone

# Setup
client = Client()
user = User.objects.create_user('loguser', 'log@test.com', 'logpass')
category = Category.objects.create(title='Log', slug='log', is_published=True)
location = Location.objects.create(name='Log', is_published=True)

post = Post.objects.create(
    title='Log Post',
    text='Log content',
    author=user,
    category=category,
    location=location,
    is_published=True,
    pub_date=timezone.now()
)

comment = Comment.objects.create(
    text='Log comment text',
    author=user,
    post=post
)

print("=== TEST WITH LOGGING ===")
client.login(username='loguser', password='logpass')

# Capture output
import io
from contextlib import redirect_stdout, redirect_stderr

f = io.StringIO()
with redirect_stdout(f), redirect_stderr(f):
    response = client.get(f'/posts/{post.id}/edit_comment/{comment.id}/')

output = f.getvalue()
print("Captured output:", output[:500] if output else "No output captured")

print(f"\nResponse status: {response.status_code}")

# Check HTML
html = response.content.decode('utf-8')
print(f"\nHTML length: {len(html)}")

if '<form' not in html:
    print("ERROR: No form tag in HTML!")
    print("\nFirst 1000 chars of HTML:")
    print(html[:1000])
    
    # Check for error messages
    if 'error' in html.lower() or 'exception' in html.lower():
        print("\nPossible error in HTML!")
else:
    print(" Form tag found in HTML")
