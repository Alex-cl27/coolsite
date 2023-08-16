from django.urls import path, re_path

from .views import *

urlpatterns = [
    path('', WomenHome.as_view(), name='home'),     # Отображение классом, метод ".as_view()" обязателен
    path('about/', about, name='about'),
    path('add_page/', AddPage.as_view(), name='add_page'),
    path('contact/', contact, name='contact'),
    path('login/', LoginUser.as_view(), name='login'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),        # Отображение классом, ".as_view()"
    path('catgory/<slug:cat_slug>/', WomenCategory.as_view(), name='category'),     # Отображение классом
]
