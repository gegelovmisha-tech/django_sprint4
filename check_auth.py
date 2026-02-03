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

client = Client()
user = User.objects.create_user('authuser', 'auth@test.com', 'authpass')
category = Category.objects.create(title='Auth', slug='auth', is_published=True)
location = Location.objects.create(name='Auth', is_published=True)

post = Post.objects.create(
    title='Auth Post',
    text='Auth content',
    author=user,
    category=category,
    location=location,
    is_published=True,
    pub_date=timezone.now()
)

comment = Comment.objects.create(
    text='Auth comment',
    author=user,
    post=post
)

print("=== AUTH CHECK ===")
print(f"User is authenticated before login: {client.session.get('_auth_user_id')}")

# Try without login first
print("\n1. WITHOUT LOGIN:")
response = client.get(f'/posts/{post.id}/edit_comment/{comment.id}/')
print(f"Status: {response.status_code}")
print(f"Is redirect: {response.status_code in [301, 302, 303, 307, 308]}")
if response.status_code in [301, 302, 303, 307, 308]:
    print(f"Redirect to: {response.get('Location')}")

# Now login
print("\n2. LOGGING IN...")
login_success = client.login(username='authuser', password='authpass')
print(f"Login success: {login_success}")
print(f"User ID in session: {client.session.get('_auth_user_id')}")

# Try with login
print("\n3. WITH LOGIN:")
response2 = client.get(f'/posts/{post.id}/edit_comment/{comment.id}/')
print(f"Status: {response2.status_code}")
print(f"Is redirect: {response2.status_code in [301, 302, 303, 307, 308]}")
if response2.status_code in [301, 302, 303, 307, 308]:
    print(f"Redirect to: {response2.get('Location')}")
    print("Following redirect...")
    response3 = client.get(response2['Location'])
    print(f"Final status: {response3.status_code}")
    print(f"Final URL: {response3.request['PATH_INFO']}")
    
    # Check if form is in final page
    html = response3.content.decode('utf-8')
    print(f"Form in HTML: {'<form' in html}")
else:
    html = response2.content.decode('utf-8')
    print(f"HTML length: {len(html)}")
    print(f"Form in HTML: {'<form' in html}")
    
    if '<form' not in html:
        print("\nFirst 500 chars of HTML:")
        print(html[:500])
