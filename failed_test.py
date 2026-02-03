# -*- coding: utf-8 -*-
"""
Тест для проверки отображения количества комментариев:
AssertionError: Убедитесь, что на главной странице под постами 
отображается количество комментариев. Число комментариев должно быть 
указано в круглых скобках.
"""

import os
import sys
import django
from pathlib import Path

# Добавляем путь к проекту
project_path = Path(__file__).parent / "blogicum"
sys.path.insert(0, str(project_path))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blogicum.settings')
django.setup()

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from blog.models import Post, Comment, Category, Location
from django.utils import timezone
import re

User = get_user_model()

class TestCommentDisplay(TestCase):
    """Проверка отображения комментариев"""
    
    def test_comment_display_on_main_page(self):
        # 1. Создаем пользователей
        user1 = User.objects.create_user(
            username='testuser1',
            password='testpass123'
        )
        user2 = User.objects.create_user(
            username='testuser2', 
            password='testpass123'
        )
        
        # 2. Создаем категорию и местоположение
        category = Category.objects.create(
            title='Test Category',
            slug='test-category',
            is_published=True,
            description='Test category description'
        )
        
        location = Location.objects.create(
            name='Test Location',
            is_published=True,
            description='Test location description'
        )
        
        # 3. Создаем пост
        post = Post.objects.create(
            title='Test Post Title For Display',
            text='This is test post content for checking comment display',
            author=user2,
            category=category,
            location=location,
            is_published=True,
            pub_date=timezone.now()
        )
        
        # 4. Создаем 3 комментария
        comments_count = 3
        for i in range(comments_count):
            Comment.objects.create(
                post=post,
                author=user1,
                text=f'Test comment number {i+1}'
            )
        
        print(f"Создан: пост '{post.title}' с {comments_count} комментариями")
        print(f"Ожидаем на главной: ({comments_count})")
        
        # 5. Получаем главную страницу
        client = Client()
        response = client.get('/')
        content = response.content.decode('utf-8')
        
        # 6. Ищем (3) в содержимом
        expected_pattern = f'\({comments_count}\)'
        matches = re.findall(re.escape(expected_pattern), content)
        
        print(f"\nНайдено вхождений (3) на главной: {len(matches)}")
        
        if len(matches) == 0:
            print("\n=== АНАЛИЗ ОШИБКИ ===")
            print(f"Длина контента: {len(content)} символов")
            
            # Ищем пост на странице
            if post.title in content:
                print(f"✓ Пост '{post.title}' найден на главной")
                
                # Находим фрагмент с постом
                pos = content.find(post.title)
                start = max(0, pos - 300)
                end = min(len(content), pos + 800)
                fragment = content[start:end]
                
                print(f"\nФрагмент HTML вокруг поста (первые 600 символов):")
                print(fragment[:600])
                
                # Ищем "комментари" в фрагменте
                if 'комментари' in fragment.lower():
                    print(f"\n✓ 'комментари' найдено в фрагменте")
                    idx = fragment.lower().find('комментари')
                    print(f"Контекст: {fragment[idx:idx+150]}")
                    
                    # Проверяем формат
                    if f'({comments_count})' not in fragment:
                        print(f"\n✗ Но формат ({comments_count}) не найден!")
                        print("Возможные варианты в фрагменте:")
                        # Ищем любые числа в скобках
                        paren_matches = re.findall(r'\(\d+\)', fragment)
                        if paren_matches:
                            print(f"Найдены: {paren_matches}")
                        else:
                            print("Нет чисел в скобках")
                else:
                    print(f"\n✗ 'комментари' не найдено в фрагменте!")
                    
                    # Что есть в карточке поста?
                    print("\nЧто есть в карточке поста?")
                    # Проверяем стандартные элементы
                    if 'card-body' in fragment:
                        print("Есть: 'card-body'")
                    if 'card-title' in fragment:
                        print("Есть: 'card-title'")
                    if 'card-text' in fragment:
                        print("Есть: 'card-text'")
                    if 'text-muted' in fragment:
                        print("Есть: 'text-muted' (возможно, мета-информация)")
                        
                        # Ищем текст мета-информации
                        meta_match = re.search(r'<small[^>]*class="text-muted"[^>]*>(.*?)</small>', 
                                             fragment, re.DOTALL)
                        if meta_match:
                            meta_text = meta_match.group(1)
                            print(f"Мета-информация: {meta_text[:200]}...")
            else:
                print(f"✗ Пост '{post.title}' не найден на главной!")
                print("Возможные причины: пост не опубликован, не в нужной категории и т.д.")
            
            # Ищем все числа в скобках на всей странице
            print(f"\n=== ВСЕ ЧИСЛА В СКОБКАХ НА СТРАНИЦЕ ===")
            all_parentheses = re.findall(r'\((\d+)\)', content)
            print(f"Все числа в скобках на странице: {all_parentheses}")
            
            print(f"\n=== РЕКОМЕНДАЦИИ ===")
            print("1. Проверьте, что в шаблоне blog/index.html или includes/post_card.html")
            print("   есть вывод количества комментариев в формате: (X)")
            print("2. Убедитесь, что комментарии передаются в контекст главной страницы")
            print("3. Проверьте, что post.comments.count используется в шаблоне")
            
            print(f"\n=== ТЕСТ ПРОВАЛЕН ===")
            self.fail(
                "Убедитесь, что на главной странице под постами "
                "отображается количество комментариев. Число комментариев должно быть указано "
                "в круглых скобках."
            )
        else:
            print(f"✓ УСПЕХ: Количество ({comments_count}) на главной отображается")
            print(f"Вхождения: {matches}")
            
            # Дополнительная проверка - убедимся, что это именно у нашего поста
            print(f"\n=== ДОПОЛНИТЕЛЬНАЯ ПРОВЕРКА ===")
            # Найдем все посты на странице и их комментарии
            post_pattern = r'<h5[^>]*>([^<]+)</h5>.*?\((\d+)\)'
            posts_found = re.findall(post_pattern, content, re.DOTALL)
            if posts_found:
                print(f"Найдено постов с комментариями: {len(posts_found)}")
                for i, (title, count) in enumerate(posts_found[:3], 1):
                    print(f"  {i}. '{title[:30]}...' - комментариев: {count}")

if __name__ == '__main__':
    # Запускаем тест
    import unittest
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCommentDisplay)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
