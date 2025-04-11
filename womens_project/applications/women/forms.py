from django import forms

from .models import WomenModel, Category


class AddPostForm(forms.ModelForm):
    class Meta:
        model = WomenModel
        fields = ['title', 'content', 'photo', 'is_published', 'category', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 50, 'rows': 5}),
        }

    category = forms.ModelChoiceField(Category.objects.all(), empty_label='Выбор категории')


class UploadPostForm(forms.Form):
    file = forms.ImageField(label='Файл')