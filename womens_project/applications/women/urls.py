from django.urls import path, register_converter
from . import views
from . import converters

register_converter(converters.FourDigitsYearConverter, 'year4')

urlpatterns = [
    path('', views.IndexPageView.as_view(), name='home'),
    path('about/', views.AboutPageView.as_view(), name='about'),
    path('addpage/', views.AddPageView.as_view(), name='add_page'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    path('post/<slug:post_slug>/', views.ShowPostView.as_view(), name='post'),
    path('category/<slug:cat_slug>/', views.ShowCategoryView.as_view(), name='category'),
    path('tag/<slug:tag_slug>/', views.ShowTagView.as_view(), name='tags'),
    path('edit/<int:pk>/', views.UpdatePageView.as_view(), name='edit_page'),
    path('delete/<int:pk>/', views.DeletePageView.as_view(), name='delete_page'),
]