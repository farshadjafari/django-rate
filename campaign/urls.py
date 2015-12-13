from django.conf.urls import patterns, url
from . import views

urlpatterns = [
    url(r'^$', 'campaign.views.home', name='home'),
    #url(r'^$', 'campaign.views.campaign', name='campaign'),
    url(r'^(?P<campaign_id>[0-9]+)/$', views.campaign, name='campaign'),
    url(r'^(?P<campaign_id>[0-9]+)/(?P<banner_id>[0-9]+)/$', views.banner, name='banner'),
]
