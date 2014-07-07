from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from shorthand.shorthand import views

# Список URL'ов для основого приложения
shorthand_urls = patterns(
    ''
)

# Глобальный список URL'ов проекта
urlpatterns = patterns(
    '',

    url(r'^$', views.HomepageView.as_view(), name='homepage'),
    url(r'^shorthands/', include(shorthand_urls), namespace='shorthand'),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^(?P<shortcut>[A-Z0-9]*)/', views.ShorthandRedirectView, name='shortcut', namespace='shorthand'),
)
