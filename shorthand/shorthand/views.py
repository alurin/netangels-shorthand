from django.views import generic
from . import forms


class HomepageView(generic.TemplateView):
    template_name = 'homepage.html'


class CreateShorthandView(generic.CreateView):
    form_class = forms.ShorthandUrlCreateForm
    template_name = 'shorthands/create.html'

    # def form_valid(self, form):
    #     form.