from django.db.models import Count
from django.core.cache import cache

from .models import *

menu = [
    {'title': "О сайте", 'url_name': 'about'},
    {'title': "Добавить статью", 'url_name': 'add_page'},
    {'title': "Обратная связь", 'url_name': 'contact'},
]


class DataMixin:
    paginate_by = 3     # Включает пагинацию по 3 элемента. Класс ListView уже содержит в себе пагинатор

    def get_user_context(self, **kwargs):
        context = kwargs

        # cats = Category.objects.all()     # Все объекты

        # low-level cache API:
        cats = cache.get('cats')
        if not cats:
            cats = Category.objects.annotate(Count('women'))    # Метод annotate() Добавляет дополнительные атрибуты, в данном случае - annotate(count()) количество постов, связанных с рубрикой
            cache.set('cats', cats, 60)

        # context['menu'] = menu
        user_menu = menu.copy()         # скрывает "Добавить статью" для неавторизованных
        if not self.request.user.is_authenticated:
            user_menu.pop(1)
        context['menu'] = user_menu
        context['cats'] = cats
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context
