from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView

from .forms import *
from .models import *
from .utils import *


# Отображение домашней страницы ("")
class WomenHome(DataMixin, ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    # extra_context = {'title': 'Главная страница'}       # Только для статического контента

    # Для динамического (и статического) контента объявляется функция get_context_data
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Главная страница')     # Из .utils.DataMixin
        return dict(list(context.items()) + list(c_def.items()))

    # Отображать только "is_published=True"
    def get_queryset(self):
        return Women.objects.filter(is_published=True)


def about(request):
    return render(request, 'women/about.html', {'menu': menu, 'title': 'О сайте'})


# Создание статьи ('add_page/')
class AddPage(DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'women/addpage.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавление статьи')     # Из .utils.DataMixin
        return dict(list(context.items()) + list(c_def.items()))


def contact(request):
    return render(request, 'women/base.html', {'menu': menu, 'title': 'О сайте'})


def login(request):
    return render(request, 'women/base.html', {'menu': menu, 'title': 'О сайте'})


class ShowPost(DataMixin, DetailView):
    model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])     # Из .utils.DataMixin
        return dict(list(context.items()) + list(c_def.items()))


# Отображение категорий ('catgory/<slug:cat_slug>/')
class WomenCategory(DataMixin, ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False     # 404 if empty

    # Для динамического (и статического) контента объявляется функция get_context_data
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Категория - ' + str(context['posts'][0].cat),
                                      cat_selected=context['posts'][0].cat_id)     # Из .utils.DataMixin
        return dict(list(context.items()) + list(c_def.items()))

    # Отображение (фильтр) только выбранной категории и "is_published=True"
    def get_queryset(self):
        return Women.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
