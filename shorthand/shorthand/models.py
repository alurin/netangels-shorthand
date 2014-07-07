from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import query
from model_utils import fields, managers
import string


# Собираем цифры которые будут использоваться для сокращенного кода
NOTATION_DIGIT = string.digits + string.ascii_uppercase

# Количество цифр в системе счисления
NOTATION_RADIX = len(NOTATION_DIGIT)


class ShorthandUrlQuerySet(query.QuerySet):
    """
    QuerySet для кратких ссылок
    """
    def order_by_popularity(self):
        """
        Сортировка по популярности

        :return: ShorthandUrlQuerySet
        """
        return self.order_by('-views_counter', 'created_at')

    def first_populars(self, count=20):
        """
        Получение queryset'а с первыми по популярности краткими ссылками.

        :param count: Количество элементов в результате, по умолчанию 20
        :return: ShorthandQuerySet Новый queryset
        """
        queryset = self.order_by_popularity()
        return queryset[:count]


class ShorthandUrl(models.Model):
    """
    Модель хранящая информацию об краткой ссылке
    """
    class Meta:
        verbose_name = 'Краткий URL'
        verbose_name_plural = 'Краткие URL\'ы'

    created_at = fields.AutoCreatedField('Дата создания')
    url = models.URLField('URL', help_text='Полный URL', null=False, blank=False)
    shortcut = models.CharField('URI', max_length=200, help_text='Краткий URI', db_index=True, default='', blank=True, editable=False)
    views_counter = models.PositiveIntegerField('Количество просмотров', default=0)

    objects = managers.PassThroughManager(ShorthandUrlQuerySet)

    @staticmethod
    def compute_shortcut(number):
        """
        Генерация сокрощенного URI

        :param number: Число, идентификатор краткой ссылки
        :return: Число в системе счисления с основанием NOTATION_DIGIT, для использования в качестве идентификатора
                 краткой ссылки
        """
        number = int(number)
        result = ""

        while number > 0:
            char = NOTATION_DIGIT[number % NOTATION_RADIX]
            result = char + result
            number = int(number / NOTATION_RADIX)

        return result

    def increment(self, commit=True):
        """
        Добавление кол-ва просмотров краткой ссылки

        :param commit: Если True, то изменения полей экземпляра модели немедленно сохраняются в БД
        :return: ShorthandUrl для fluent-интерфейса
        """
        self.views_counter += 1
        if commit:
            self.save()
        return self
    
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        """
        Переопределяем метод сохранения для генерации уникального
        """
        super(ShorthandUrl, self).save(force_insert=force_insert, force_update=force_update, using=using,
                                       update_fields=update_fields)

        if not self.shortcut and self.id:
            self.shortcut = ShorthandUrl.compute_shortcut(self.id)
            self.save()

    def get_full_url(self, request):
        """
        Получение полного URL на сайте относительно запроса
        """
        return "http://%s/%s" % (request.hostname, self.shortcut)

    def get_redirect_url(self):
        return reverse('shortcut-redirect', kwargs={'shortcut': self.shortcut})

    def get_absolute_url(self):
        return reverse('shorthand:detail', kwargs={'pk': self.id})

    def __str__(self):
        return self.shortcut

    def __repr__(self):
        return '<%s.%s: %s>' % (self.__class__.__module__, self.__class__.__name__, self.shortcut)