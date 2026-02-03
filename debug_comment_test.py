# -*- coding: utf-8 -*-
import os
import sys
import pytest

# Сохраним оригинальный тест для monkey-patch
original_test = None

# Добавляем путь для импорта
sys.path.insert(0, '.')
import tests.test_comment as test_module

# Находим функцию test_comment
for name in dir(test_module):
    if name == 'test_comment':
        original_test = getattr(test_module, name)
        break

if original_test:
    # Декоратор для отладки теста
    def debug_test(*args, **kwargs):
        print("=== ЗАПУСК ТЕСТА ===")
        try:
            result = original_test(*args, **kwargs)
            print("=== ТЕСТ ПРОЙДЕН ===")
            return result
        except AssertionError as e:
            print(f"\n=== ОШИБКА В ТЕСТЕ ===")
            print(f"Сообщение: {e}")
            
            # Пытаемся понять, где проблема
            print(f"\n=== АНАЛИЗ ПРОБЛЕМЫ ===")
            
            # Получаем клиента и пост из аргументов
            user_client = kwargs.get('user_client') or args[0]
            post_with_published_location = kwargs.get('post_with_published_location') or args[3]
            
            # Проверяем главную страницу
            response = user_client.get("/")
            content = response.content.decode('utf-8')
            
            print(f"Длина главной страницы: {len(content)} символов")
            
            # Ищем числа в скобках (количество комментариев)
            import re
            matches = re.findall(r'\((\d+)\)', content)
            print(f"Все числа в скобках на главной: {matches}")
            
            # Проверяем пост
            if hasattr(post_with_published_location, 'title'):
                post_title = post_with_published_location.title
                print(f"\nТестовый пост: {post_title}")
                
                if post_title in content:
                    print(f"✓ Пост найден на главной")
                    pos = content.find(post_title)
                    fragment = content[max(0, pos-200):min(len(content), pos+500)]
                    
                    print(f"\nФрагмент вокруг поста (первые 400 символов):")
                    print(fragment[:400])
                    
                    # Ищем "комментари"
                    if 'комментари' in fragment.lower():
                        idx = fragment.lower().find('комментари')
                        print(f"\nКонтекст 'комментари': {fragment[idx:idx+100]}")
                    else:
                        print(f"\n✗ 'комментари' не найдено в фрагменте!")
                        
                        # Что есть в карточке?
                        print("Что есть в карточке поста:")
                        lines = fragment.split('\n')
                        for line in lines:
                            if 'card-link' in line or 'card-text' in line or 'text-muted' in line:
                                print(f"  {line.strip()[:100]}")
                else:
                    print(f"✗ Пост не найден на главной!")
            
            print(f"\n=== ПРОВЕРКА СТРАНИЦЫ ПОЛЬЗОВАТЕЛЯ ===")
            if hasattr(post_with_published_location, 'author'):
                author = post_with_published_location.author
                profile_url = f'/profile/{author.username}/'
                response = user_client.get(profile_url)
                content = response.content.decode('utf-8')
                
                if post_title in content:
                    print(f"✓ Пост найден на странице пользователя")
                    # Ищем числа в скобках
                    matches = re.findall(r'\((\d+)\)', content)
                    print(f"Числа в скобках на странице профиля: {matches}")
                else:
                    print(f"✗ Пост не найден на странице пользователя")
            
            print(f"\n=== РЕКОМЕНДАЦИИ ===")
            print("1. Проверьте шаблоны:")
            print("   - blog/index.html (главная страница)")
            print("   - blog/profile.html (страница пользователя)")
            print("   - includes/post_card.html (если используется)")
            print("2. Убедитесь, что в шаблонах есть: {{ post.comments.count }} или аналогичное")
            print("3. Формат должен быть: (X) где X - число комментариев")
            
            raise
        except Exception as e:
            print(f"\n=== НЕОЖИДАННАЯ ОШИБКА ===")
            print(f"{type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    # Заменяем тест в модуле
    setattr(test_module, 'test_comment', debug_test)

# Запускаем pytest с нашим отладочным тестом
if __name__ == '__main__':
    pytest.main(['tests/test_comment.py::test_comment', '-v', '-s', '--tb=short'])
