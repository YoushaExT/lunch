from django.urls import path, include

from django.contrib import admin

admin.autodiscover()

from khana.admin import admin_site

import khana.views
# To add a new path, first import the app:
# import blog
#
# Then add the new path:
# path('blog/', blog.urls, name="blog")
#
# Learn more here: https://docs.djangoproject.com/en/2.1/topics/http/urls/

urlpatterns = [
    path('', khana.views.index),
    path("admin/", admin.site.urls),
    path('khana/', include('khana.urls')),
    path('myadmin/', admin_site.urls),
    path('<str:useless>', khana.views.default),
    # path('accounts/', include('django.contrib.auth.urls')),
]
