# -*- coding: utf-8 -*-
import re

with open('blogicum/templates/includes/header.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Старая форма для выхода
old_form = '''<form action="{% url 'logout' %}" method="post" style="display: inline;">
          {% csrf_token %}
          <button type="submit" class="btn btn-link" style="padding: 0; border: none; background: none; color: #000;">
            Выйти
          </button>
        </form>'''

new_form = '''<!-- Скрытая форма для выхода -->
        <form id="logout-form" action="{% url 'logout' %}" method="post" style="display: none;">
          {% csrf_token %}
        </form>
        <!-- Ссылка для выхода -->
        <a href="#" onclick="document.getElementById('logout-form').submit(); return false;" 
           class="btn btn-link" style="padding: 0; border: none; background: none; color: #000;">
          Выйти
        </a>'''

if old_form in content:
    content = content.replace(old_form, new_form)
    with open('blogicum/templates/includes/header.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print('Форма выхода заменена на скрытую форму + ссылку')
else:
    print('Не найдена старая форма выхода. Ищем другую форму...')
    
    # Поищем любую форму с logout
    logout_pattern = r'(<form[^>]*?action="{% url \'logout\' %}"[^>]*?>.*?</form>)'
    match = re.search(logout_pattern, content, flags=re.DOTALL)
    
    if match:
        print(f'Найдена форма выхода, заменяем...')
        content = re.sub(logout_pattern, new_form, content, flags=re.DOTALL)
        with open('blogicum/templates/includes/header.html', 'w', encoding='utf-8') as f:
            f.write(content)
        print('Форма выхода заменена на скрытую форму + ссылку')
    else:
        print('Не найдено форм с logout. Проверяем наличие кнопки Выйти...')
        
        # Если есть просто кнопка "Выйти", добавляем нашу реализацию
        if 'Выйти</button>' in content or 'Выйти</a>' in content:
            # Заменяем любую кнопку/ссылку Выйти
            content = re.sub(
                r'(<[^>]*?>[^<]*?Выйти[^<]*?</[^>]*?>)',
                new_form,
                content
            )
            with open('blogicum/templates/includes/header.html', 'w', encoding='utf-8') as f:
                f.write(content)
            print('Кнопка "Выйти" заменена на скрытую форму + ссылку')
        else:
            print('Не найдено элементов выхода. Оставляем как есть.')
