from django.views import generic
from django.views.generic import detail
from . import forms
from . import models


class HomepageView(generic.TemplateView):
    """
    Данный вид отображает главную страницу сайта

    :notice: Данный класс унаследован от TemplateView для расширения возможностей данного вида в дальнейшем.
    """
    template_name = 'homepage.html'

    def get_context_data(self, **kwargs):
        context = super(HomepageView, self).get_context_data(**kwargs)
        context.update({
            'form': forms.ShorthandUrlCreateForm(),
            'popular_shorthands': models.ShorthandUrl.objects.first_populars(),
        })
        return context


class ShorthandUrlCreateView(generic.CreateView):
    """
    Обработчик создания краткой ссылки
    """
    form_class = forms.ShorthandUrlCreateForm
    template_name = 'shorthands/create.html'


class ShorthandUrlDetailView(generic.DetailView):
    model = models.ShorthandUrl
    template_name = 'shorthands/detail.html'


class ShorthandUrlListView(generic.ListView):
    model = models.ShorthandUrl
    template_name = 'shorthands/list.html'
    paginate_by = 10

    def get_queryset(self):
        return super(ShorthandUrlListView, self).get_queryset().order_by_popularity()


class ShorthandUrlRedirectView(generic.RedirectView, detail.SingleObjectMixin):
    """
    Данный вид редиректит агента пользователя c краткой ссылки на полную. В качестве побочного эфекта увлечивается
    её количество просмотров.

    :notice: Заместо `slug` использован `shortcut`.
    :notice: В задании не чего не было сказано про способ редиректа, поэтому для лучшей отладки `permanent` выставлен
             в False
    """
    model = models.ShorthandUrl
    slug_field = 'shortcut'
    slug_url_kwarg = 'shortcut'
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        short = self.get_object()
        short.increment()
        return short.url
