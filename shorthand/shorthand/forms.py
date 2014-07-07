from django import forms
from . import models


class ShorthandUrlCreateForm(forms.ModelForm):
    """
    Форма для создания нового сокрощенного URL'а
    """
    class Meta:
        model = models.ShorthandUrl
        fields = ('url',)