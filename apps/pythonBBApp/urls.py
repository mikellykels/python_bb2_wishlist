from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register$', views.register, name='register'),
    url(r'^login$', views.login, name='login'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^wishlist/dashboard$', views.dashboard, name='dashboard'),
    url(r'^wishlist/add$', views.add, name='add'),
    url(r'^wishlist/create$', views.create, name='create'),
    url(r'^wishlist/(?P<item_id>[0-9]*)$', views.show_item, name='show_item'),
    url(r'^wishlist/delete/(?P<item_id>[0-9]*)$', views.delete, name='delete'),
    url(r'^wishlist/remove/(?P<item_id>[0-9]*)$', views.remove, name='remove')
]
