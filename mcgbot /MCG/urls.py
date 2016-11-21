from django.conf.urls import url

from MCG.views import index

urlpatterns = [
               #url(r'^$', views.index, name='index'),
               url(r'^$', index.as_view()),
               ]
