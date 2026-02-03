# Register your models here.
# Импортируем административный модуль Django
from django.contrib import admin

# Импортируем наши модели из текущего приложения
from .models import Category, Location, Post


# Регистрируем модель Category с настройками
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # Какие поля показывать в списке категорий
    list_display = ('title', 'is_published', 'created_at')
    # Какие поля можно редактировать прямо в списке
    # (без захода в каждую категорию)
    list_editable = ('is_published',)
    # По каким полям можно искать (появится строка поиска)
    search_fields = ('title', 'description')


# Регистрируем модель Location с настройками
@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_published', 'created_at')
    list_editable = ('is_published',)
    search_fields = ('name',)


# Регистрируем модель Post с настройками
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # Какие поля показывать в списке постов
    list_display = (
        'title',           # Заголовок
        'pub_date',        # Дата публикации
        'author',          # Автор
        'category',        # Категория
        'location',        # Местоположение
        'is_published',    # Опубликовано или нет
        'created_at'       # Дата создания
    )
    # Какие поля можно редактировать прямо в списке
    list_editable = ('is_published', 'category', 'location')
    # По каким полям можно искать
    search_fields = ('title', 'text')
    # Фильтры справа (для быстрой фильтрации постов)
    list_filter = ('category', 'location', 'is_published', 'pub_date')
    # Навигация по датам вверху
    date_hierarchy = 'pub_date'
