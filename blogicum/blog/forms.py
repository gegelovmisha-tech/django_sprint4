from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import Comment, Post

User = get_user_model()


class CreationForm(UserCreationForm):
    class Meta:  # ← ИСПРАВИТЬ: убрать (UserCreationForm.Meta)
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'pub_date', 'image', 'category', 'location']
        widgets = {
            'pub_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'text': forms.Textarea(attrs={'rows': 4}),
        }
        help_texts = {
            'pub_date': 'Для отложенной публикации установите дату в будущем',
            'image': 'Загрузите изображение для публикации',
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Оставьте комментарий...'
            }),
        }
