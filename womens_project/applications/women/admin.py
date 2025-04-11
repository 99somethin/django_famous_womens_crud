from django.contrib import admin, messages
from applications.women.models import WomenModel, TagPost, Category
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from django.urls import reverse

# Register your models here.
@admin.register(WomenModel)
class WomenAdmin(admin.ModelAdmin):
    fields = ['title', 'content', 'category', 'slug', 'post_photo', 'photo', 'tags']
    readonly_fields = ['slug', 'post_photo']
    list_display = ('title', 'time_create', 'is_published', 'category', 'post_photo', 'delete_button')
    list_display_links = ('title', )
    actions = ['set_published', 'set_draft']
    search_fields = ['title']
    list_filter = ['category__name', 'is_published']
    save_on_top = True

    list_editable = ('is_published', )

    def delete_button(self, obj):
        return format_html(
            '<a class="button" href="{}">Delete</a>',
            reverse('admin:%s_%s_delete' % (obj._meta.app_label, obj._meta.model_name), args=[obj.pk])
        )

    @admin.display(description='Фото')
    def post_photo(self, women: WomenModel):
        if women.photo:
            return mark_safe(f'<img src="{women.photo.url}" width=50>')
        else:
            return 'Нет фотографии'

    @admin.action(description='Опубликовать выбранные записи')
    def set_published(self, request, queryset):
        count = queryset.update(is_published=WomenModel.Status.PUBLISHED)
        self.message_user(request, f'Изменено {count} записей')

    @admin.action(description='Архивировать выбранные записи')
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=WomenModel.Status.DRAFT)
        self.message_user(request, f'Изменено {count} записей', messages.WARNING)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name')
    class Meta:
        fields = '__all__'

