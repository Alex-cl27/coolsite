from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

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
        # .select_related('cat') - загрузка связанных ключей, что бы убрать дубликаты sql запросов
        return Women.objects.filter(is_published=True).select_related('cat')


def about(request):
    return render(request, 'women/about.html', {'menu': menu, 'title': 'О сайте'})


# Создание статьи ('add_page/')
class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')      # В случае успеха отправляет на 'home'
    login_url = reverse_lazy('home')        # Перенаправляет неавторизованных на 'home'
    raise_exception = True                  # Генерировать 403 для неавторизованных

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавление статьи')     # Из .utils.DataMixin
        return dict(list(context.items()) + list(c_def.items()))


def contact(request):
    # return render(request, 'women/base.html', {'menu': menu, 'title': 'Обратная связь'})
    return HttpResponse("Обратная связь")


# def login(request):
#     # return render(request, 'women/base.html', {'menu': menu, 'title': 'Авторизация'})
#     return HttpResponse("Авторизация")


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
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Категория - ' + str(c.name),
                                      cat_selected=c.pk)
        return dict(list(context.items()) + list(c_def.items()))

    # Отображение (фильтр) только выбранной категории и "is_published=True"
    def get_queryset(self):
        # .select_related('cat') - загрузка связанных ключей, что бы убрать дубликаты sql запросов
        return Women.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'women/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')     # Из .utils.DataMixin
        return dict(list(context.items()) + list(c_def.items()))

    # Вызывается при успешной проверке формы регистрации
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm      # custom form
    template_name = 'women/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация')
        return dict(list(context.items()) + list(c_def.items()))

    # Логин редирект. Дублируется в settings.LOGIN_REDIRECT
    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')
