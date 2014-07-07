from django.db import models


class ShorthandUrl(models.Model):
    """
    Модель хранящая информацию об сокращенном URL'е
    """
    class Meta:
        verbose_name = 'Сокращенный URL'
        verbose_name_plural = 'Сокращенные URL\'ы'

    url = models.URLField('URL', help_text='Полный URL')
    shortcut = models.CharField('Сокрощение', help_text='Сокрощенный URI', unique=True)
    views_counter = models.PositiveIntegerField('Количество просмотров', default=0)

    def increment(self, commit=True):
        """
        Добавление кол-ва просмотров сокращенного URL'а

        :param commit: Если True, то изменения полей экземпляра модели немедленно сохраняются в БД
        :return:
        """
        self.views_counter += 1
        if commit:
            self.save()