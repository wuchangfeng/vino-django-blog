from django.conf.urls import url
from . import views
from django.conf import settings
from django.views.generic.base import RedirectView

favicon_view = RedirectView.as_view(url='/static/favicon.ico', permanent=True)


urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^article/(?P<article_id>\d+)$', views.ArticleDetailView.as_view(), name='detail'),
    url(r'^category/(?P<category_id>\d+)$', views.CategoryView.as_view(), name='category'),
    url(r'^tag/(?P<tag_id>\d+)$', views.TagView.as_view(), name='tag'),
    url(r'^favicon.ico$', favicon_view),
    url(r'^search/$', views.SearchView.as_view(), name='search'),
]
