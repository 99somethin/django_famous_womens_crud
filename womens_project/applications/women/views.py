from audioop import reverse

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.paginator import Paginator
from django.db import connection
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template.context_processors import request
from django.template.defaultfilters import title
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, FormView, CreateView, UpdateView, DeleteView
from unicodedata import category

from .models import WomenModel, TagPost, UploadFilesModel
from .forms import AddPostForm, UploadPostForm
from .utils import DataMixin

# Create your views here.
menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}]


class IndexPageView(DataMixin, ListView):
    model = WomenModel
    template_name = 'women/index.html'
    context_object_name = 'posts'
    title_page = 'Главная страница'

    def get_queryset(self):
        return WomenModel.published.all().select_related('category')


class AboutPageView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        contact_list = WomenModel.published.all()
        paginator = Paginator(contact_list, 3)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'women/about.html',
                      {'title': 'О сайте', 'page_obj': page_obj})


class ShowPostView(DataMixin, DetailView):
    model = WomenModel
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'data'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return self.get_mixin_context(context, title=context['data'].title)

    def get_object(self, queryset=None):
        return get_object_or_404(WomenModel.published, slug=self.kwargs[self.slug_url_kwarg])


class AddPageView(PermissionRequiredMixin, LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')
    title_page = 'Добавление статьи'
    permission_required = 'applications.women.add_women'

    def form_valid(self, form):
        w = form.save(commit=False)
        w.author = self.request.user
        return super().form_valid(form)


class UpdatePageView(UpdateView):
    model = WomenModel
    fields = ['title', 'content', 'photo', 'is_published', 'category']
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')
    title_page = 'Обновление записи'


class DeletePageView(DeleteView):
    model = WomenModel
    template_name = 'women/delete.html'
    success_url = reverse_lazy('home')


def contact(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Авторизация")


def error_404_view(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


class ShowCategoryView(DataMixin, ListView):
    model = WomenModel
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = True

    def get_queryset(self):
        return WomenModel.published.filter(category__slug=self.kwargs['cat_slug']).select_related('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].category
        return self.get_mixin_context(context, title='Категория - ' + cat.name, category_selected=cat.slug)


class ShowTagView(DataMixin, ListView):
    model = WomenModel
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = True

    def get_queryset(self):
        return WomenModel.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        return self.get_mixin_context(context, title='Тег - ' + tag.tag, )
