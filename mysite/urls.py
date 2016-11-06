
from django.conf.urls import include, url
from django.contrib import admin
from blog.views import IndexView as IndexView
from blog.views import about_me as about_me
from blog.views import archives as archives
from blog.views import comments as comments


urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^blog/', include('blog.urls', namespace='blog')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^about/', about_me, name='about_me'),
    url(r'^archives/$', archives, name = 'archives'),
    url(r'^comments/$', comments, name = 'comments'),
]
