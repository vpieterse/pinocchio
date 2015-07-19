# from django.conf.urls import include, url
# from django.contrib import admin

# urlpatterns = [
#     # Examples:
#     # url(r'^$', 'pinocchio.views.home', name='home'),
#     # url(r'^blog/', include('blog.urls')),
#     url(r'^peer/', include('peer_review.urls')),
#     url(r'^admin/', include(admin.site.urls)),
#     url(r'^myapp/', include('myapp.urls')),
# ]

# # -*- coding: utf-8 -*-
# from django.conf.urls import patterns, include, url
# from django.conf import settings
# from django.conf.urls.static import static
# from django.views.generic import RedirectView
# from django.contrib import admin

# urlpatterns = patterns('',
# 	(r'^peer/', include('peer_review.urls')),
# 	(r'^admin/', include(admin.site.urls)),
# 	(r'^myapp/', include('myapp.urls')),
# 	(r'^$', RedirectView.as_view(url='/myapp/list/')), # Just for ease of use.
# ) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import RedirectView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # Examples:
    # url(r'^$', 'pinocchio.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^peer/', include('peer_review.urls')),
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^', RedirectView.as_view(url='/myapp/list/')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)