from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^$', 'campaign.views.home', name='home'),
    url(r'^campaign/', include('campaign.urls')),
    url(r'^admin/', admin.site.urls),
]
