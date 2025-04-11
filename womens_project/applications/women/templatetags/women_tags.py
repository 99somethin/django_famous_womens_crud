from django import template
from django.db.models import Count, Q
from applications.women.models import Category, TagPost, WomenModel
from .. import utils

register = template.Library()

@register.simple_tag
def get_menu():
    return utils.DataMixin.menu

@register.inclusion_tag('women/list_categories.html')
def show_category(category_selected = None):
    data = Category.objects.annotate(category_count=Count('posts')).filter(Q(category_count__gte=1) \
        & Q(posts__is_published=WomenModel.Status.PUBLISHED))
    return {'categories': data, 'category_selected': category_selected}

@register.inclusion_tag('women/list_tags.html')
def show_all_tags():
    tags = TagPost.objects.annotate(tag_count=Count('tags')).filter(Q(tag_count__gte=1) & \
        Q(tags__is_published=WomenModel.Status.PUBLISHED))
    return {'tags': tags }


