# -*- coding: utf-8 -*-
import os
import sys
import subprocess

def check_project():
    print("=== ПРОВЕРКА ПРОЕКТА БЛОГИКУМ ===")
    print()
    
    # 1. Проверка URL для комментариев
    print("1. URL ДЛЯ КОММЕНТАРИЕВ:")
    result = subprocess.run(
        ["grep", "-q", "edit_comment.*delete_comment", "blogicum/blog/urls.py"],
        capture_output=True
    )
    
    if result.returncode == 0:
        print("✓ URL для комментариев найдены")
        result = subprocess.run(
            ["grep", "edit_comment\|delete_comment", "blogicum/blog/urls.py"],
            capture_output=True,
            text=True
        )
        print(result.stdout)
    else:
        print("✗ URL для комментариев НЕ найдены")
    print()
    
    # 2. Проверка представлений для комментариев
    print("2. ПРЕДСТАВЛЕНИЯ ДЛЯ КОММЕНТАРИЕВ:")
    result = subprocess.run(
        ["grep", "-q", "def.*edit_comment\|def.*delete_comment", "blogicum/blog/views.py"],
        capture_output=True
    )
    
    if result.returncode == 0:
        print("✓ Функции для комментариев найдены")
        result = subprocess.run(
            ["grep", "-n", "def.*edit_comment\|def.*delete_comment", "blogicum/blog/views.py"],
            capture_output=True,
            text=True
        )
        print(result.stdout)
    else:
        print("✗ Функции для комментариев НЕ найдены")
    print()
    
    # 3. Проверка модели Comment
    print("3. МОДЕЛЬ COMMENT:")
    result = subprocess.run(
        ["grep", "-q", "class Comment", "blogicum/blog/models.py"],
        capture_output=True
    )
    
    if result.returncode == 0:
        print("✓ Модель Comment существует")
        result = subprocess.run(
            ["grep", "-n", "class Comment", "blogicum/blog/models.py", "-A", "5"],
            capture_output=True,
            text=True
        )
        print(result.stdout)
    else:
        print("✗ Модель Comment НЕ существует")
    print()
    
    # 4. Проверка доступа к постам в detail view
    print("4. ДОСТУП К ПОСТАМ В DETAIL VIEW:")
    result = subprocess.run(
        ["grep", "-n", "def detail", "blogicum/blog/views.py"],
        capture_output=True,
        text=True
    )
    
    if result.stdout:
        print("✓ Функция detail существует")
        detail_start = result.stdout.split(':')[0]
        detail_start = int(detail_start)
        detail_end = detail_start + 30
        
        print("--- Код функции detail (первые 30 строк):")
        
        # Получаем строки из файла
        with open('blogicum/blog/views.py', 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Выводим нужные строки с фильтрацией
        for i in range(detail_start - 1, min(detail_end - 1, len(lines))):
            line = lines[i]
            if any(keyword in line for keyword in ['if', 'is_published', 'category', 'author', '404', 'Http404']):
                print(f"  Строка {i+1}: {line.rstrip()}")
    else:
        print("✗ Функция detail НЕ существует")
    print()
    
    # 5. Проверка ссылок в шаблоне detail.html
    print("5. ССЫЛКИ В ШАБЛОНЕ DETAIL.HTML:")
    
    # Сначала пробуем найти с русскими словами
    result = subprocess.run(
        ["grep", "-q", "-i", "edit_comment.*delete_comment", "blogicum/templates/blog/detail.html"],
        capture_output=True
    )
    
    if result.returncode == 0:
        print("✓ Ссылки на редактирование/удаление комментариев найдены")
        result = subprocess.run(
            ["grep", "-n", "-i", "edit.*comment\|delete.*comment", "blogicum/templates/blog/detail.html"],
            capture_output=True,
            text=True
        )
        print(result.stdout)
    else:
        # Если не нашли, проверяем наличие комментариев
        print("✗ Ссылки на редактирование/удаление комментариев НЕ найдены")
        print("Содержимое detail.html (фрагмент):")
        result = subprocess.run(
            ["grep", "-n", "comment", "blogicum/templates/blog/detail.html", "|", "head", "-10"],
            shell=True,
            capture_output=True,
            text=True
        )
        print(result.stdout)

if __name__ == "__main__":
    check_project()
