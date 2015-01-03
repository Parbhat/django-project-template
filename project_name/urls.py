from django.conf import settings
from django.conf.urls import patterns, url, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = patterns('',
)

if settings.DEBUG:
    # for static assets during development
    urlpatterns += staticfiles_urlpatterns()
