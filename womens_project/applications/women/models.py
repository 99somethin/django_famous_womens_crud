from cProfile import label

from django.utils.deconstruct import deconstructible
from django.db import models
from django.template.defaultfilters import slugify, default
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model


# Create your models here.

@deconstructible
class RussianValidator:
    code = 'russian'
    allowed_chars = 'абвгдежзийклмнопрстуфхцчшщъыьэюя ' + 'абвгдежзийклмнопрстуфхцчшщъыьэюя'.upper()

    def __init__(self, message = None):
        self.message = message if message else ('Только русские символы, дефис и пробел')

    def __call__(self, value, *args, **kwargs):
        if not (set(value) <= set(self.allowed_chars)):
            raise ValidationError(self.message, code=self.code)


def translit_to_eng(s: str) -> str:
    d = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd',
         'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i', 'к': 'k',
         'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
         'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'c', 'ч': 'ch',
         'ш': 'sh', 'щ': 'shch', 'ь': '', 'ы': 'y', 'ъ': '', 'э': 'r', 'ю': 'yu', 'я': 'ya'}

    return "".join(map(lambda x: d[x] if d.get(x, False) else x, s.lower()))

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published= WomenModel.Status.PUBLISHED)


class WomenModel(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    title = models.CharField(max_length=50, validators=[RussianValidator()], verbose_name='Заголовок')
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    content = models.TextField(blank=True, verbose_name='Текст статьи')
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default = Status.DRAFT,
                                       choices=tuple(map(lambda x: (bool(x[0]), x[1]) ,Status.choices)))
    category = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='posts')
    tags = models.ManyToManyField('TagPost', related_name='tags',blank=True)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', default=None, blank=True, null=True, verbose_name='photo')
    husbend = models.OneToOneField('HusbendModel', on_delete=models.SET_NULL, null=True, blank=True, related_name='women')
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name='posts', null=True, default=None)

    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    class Meta:
        verbose_name = 'Известные женщины'
        verbose_name_plural = 'Известные женщины'
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create'])
        ]

    def save(self, *args, **kwargs):
        self.slug = slugify(translit_to_eng(str(self.title)))
        super().save(*args, **kwargs)


class Category(models.Model):
    class Meta:
        verbose_name = 'Категории'
        verbose_name_plural = 'Категории'
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(unique=True, max_length=255, db_index=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})



class TagPost(models.Model):
    tag = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True, db_index=True)

    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        return reverse('tags', kwargs={'tag_slug': self.slug})


class HusbendModel(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(null=True)

    def __str__(self):
        return self.name


class UploadFilesModel(models.Model):
    file = models.FileField(upload_to='uploads_model')





