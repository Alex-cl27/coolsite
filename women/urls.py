from django.urls import path, re_path, include
from django.views.decorators.cache import cache_page

from .views import *

urlpatterns = [
    # Отображение классом, метод ".as_view()" обязателен; cache_page(60) - кэш-страница
    path('', WomenHome.as_view(), name='home'),

    path('about/', About.as_view(), name='about'),
    path('add_page/', AddPage.as_view(), name='add_page'),
    path('contact/', ContactFormView.as_view(), name='contact'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),        # Отображение классом, ".as_view()"
    path('catgory/<slug:cat_slug>/', WomenCategory.as_view(), name='category'),     # Отображение классом
]
