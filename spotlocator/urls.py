from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^customer_dash/$', views.customer_dash, name='customer_dash'),
    url(r'^create_menu/$', views.create_menu, name='create_menu'),
    url(r'^menulist/$', views.menu_list, name='menu_list'),
    #url(r'^menulist/(?P<menu_id>[0-9]+)/detail/$', views.menu_details, name='menu_detail'),
    #url(r'^sharwama/menu/$', views.menu_details, name='menu_detail'),
    url(r'^owners_profile/$', views.owners_profiles, name='owners_profile'),
    url(r'^login_user/$', views.login_view, name='login_user'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^user_register/$', views.register, name='register'),
]

