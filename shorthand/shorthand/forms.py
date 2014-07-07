from django import forms
from . import models


class ShorthandUrlCreateForm(forms.ModelForm):
    """
    Форма для создания нового краткой ссылки
    """
    class Meta:
        model = models.ShorthandUrl
        fields = ('url',)