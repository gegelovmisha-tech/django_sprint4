# -*- coding: utf-8 -*-
import re

with open('blogicum/templates/blog/detail.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Заменяем форму удаления комментария на ссылку
# Упрощенный паттерн для поиска формы удаления
delete_pattern = r'(<form method="post" action="{% url \'blog:delete_comment\' post\.id comment\.id %}" style="display: inline;">\s*{% csrf_token %}\s*<button type="submit" class="btn btn-sm btn-outline-danger">[^<]+</button>\s*</form>)'
delete_replacement = '<a href="{% url \'blog:delete_comment\' post.id comment.id %}" class="btn btn-sm btn-outline-danger">Удалить</a>'

# Если не находит, попробуем другой паттерн
if not re.search(delete_pattern, content):
    # Паттерн для кракозябр (если текст кнопки в неправильной кодировке)
    delete_pattern = r'(<form method="post" action="{% url \'blog:delete_comment\' post\.id comment\.id %}" style="display: inline;">\s*{% csrf_token %}\s*<button type="submit" class="btn btn-sm btn-outline-danger">.*?</button>\s*</form>)'
    delete_replacement = '<a href="{% url \'blog:delete_comment\' post.id comment.id %}" class="btn btn-sm btn-outline-danger">Удалить</a>'

new_content = re.sub(delete_pattern, delete_replacement, content, flags=re.DOTALL)

# 2. Исправляем условие для формы добавления комментария
# Меняем: {% if not editing_comment and user.is_authenticated %}
# На:     {% if not editing_comment and user.is_authenticated and not confirm_delete_comment %}
add_comment_pattern = r'(\{% if not editing_comment and user\.is_authenticated %\})'
add_comment_replacement = '{% if not editing_comment and user.is_authenticated and not confirm_delete_comment %}'

if re.search(add_comment_pattern, new_content):
    new_content = re.sub(add_comment_pattern, add_comment_replacement, new_content)
else:
    # Если уже исправлено, проверяем
    if 'and not confirm_delete_comment' not in new_content:
        # Ищем другой вариант
        add_comment_pattern = r'(\{% if not editing_comment and user\.is_authenticated and[^%]+%\})'
        new_content = re.sub(add_comment_pattern, '{% if not editing_comment and user.is_authenticated and not confirm_delete_comment %}', new_content)

# 3. Проверяем, что форма редактирования существует
if '{% if editing_comment and editing_comment.id == comment.id %}' in new_content:
    print("✓ Блок редактирования найден в шаблоне")
else:
    print("✗ ВНИМАНИЕ: Блок редактирования не найден в шаблоне!")
    print("  Нужно добавить:")
    print('  {% if editing_comment and editing_comment.id == comment.id %}')
    print('    <form method="post" action="{% url \'blog:edit_comment\' post.id comment.id %}">')
    print('      {% csrf_token %}')
    print('      {% bootstrap_form comment_form %}')
    print('      <button type="submit" class="btn btn-primary">Сохранить</button>')
    print('    </form>')
    print('  {% endif %}')

# 4. Проверяем, что ссылки редактирования и удаления разные
edit_count = len(re.findall(r'href="{% url \'blog:edit_comment\'', new_content))
delete_count = len(re.findall(r'href="{% url \'blog:delete_comment\'', new_content))

if edit_count > 0 and delete_count > 0:
    print(f"✓ Найдено ссылок: редактирование={edit_count}, удаление={delete_count}")
elif 'Редактировать</a>' in new_content and 'Удалить</a>' in new_content:
    print("✓ Ссылки 'Редактировать' и 'Удалить' найдены")
else:
    print("✗ Проблема: нужно убедиться, что есть ОБЕ ссылки: Редактировать и Удалить")

# Сохраняем исправленный файл
with open('blogicum/templates/blog/detail.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("\n✓ Шаблон detail.html исправлен!")
print("\nПроверьте ключевые моменты:")
print("1. Форма удаления заменена на ссылку")
print("2. Добавлена проверка 'and not confirm_delete_comment' для формы добавления")
print("3. Форма редактирования должна быть видна при editing_comment")
