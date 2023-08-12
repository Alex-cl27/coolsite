from django.urls import path, re_path

from .views import *

urlpatterns = [
    path('', WomenHome.as_view(), name='home'),     # Отображение классом, метод ".as_view()" обязателен
    # path('', index, name='home'),                 # Отображение функцией
    path('about/', about, name='about'),
    path('add_page/', AddPage.as_view(), name='add_page'),
    # path('add_page/', add_page, name='add_page'),
    path('contact/', contact, name='contact'),
    path('login/', login, name='login'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),        # Отображение классом, ".as_view()"
    # path('post/<slug:post_slug>/', show_post, name='post'),
    path('catgory/<slug:cat_slug>/', WomenCategory.as_view(), name='category'),     # Отображение классом
    # path('catgory/<slug:cat_slug>/', show_category, name='category'),             # Отображение функцией
]
