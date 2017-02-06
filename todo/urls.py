from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^', include('django.contrib.auth.urls', namespace='auth')),
    url(r'^', include('core.urls')),
]

urlpatterns += staticfiles_urlpatterns()
