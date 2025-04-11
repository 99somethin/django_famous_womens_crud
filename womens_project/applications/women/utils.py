

class DataMixin:
    title_page = None
    extra_context = {}
    category_selected = None
    paginate_by = 3

    menu = [{'title': "О сайте", 'url_name': 'about'},
            {'title': "Добавить статью", 'url_name': 'add_page'},
            {'title': "Обратная связь", 'url_name': 'contact'}]

    def __init__(self):
        if self.title_page:
            self.extra_context['title'] = self.title_page

        if self.category_selected is not None:
            self.extra_context['category_selected'] = self.category_selected

    def get_mixin_context(self, context, **kwargs):
        context['category_selected'] = None
        context.update(kwargs)
        return context