from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from shorthand.shorthand import views

# Список URL'ов для основого приложения
shorthand_urls = patterns(
    '',

    url(r'^$', views.ShorthandUrlListView.as_view(), name='list'),

    url(r'^(?P<pk>\d+)/$', views.ShorthandUrlDetailView.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/delete$', views.ShorthandUrlDeleteView.as_view(), name='delete'),

    url(r'^create/$', views.ShorthandUrlCreateView.as_view(), name='create'),
)

# Глобальный список URL'ов проекта
urlpatterns = patterns(
    '',

    url(r'^$', views.HomepageView.as_view(), name='homepage'),
    url(r'^shorthands/', include(shorthand_urls, namespace='shorthand')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^(?P<shortcut>[A-Z0-9]*)/', views.ShorthandUrlRedirectView.as_view(), name='shortcut-redirect'),
)
