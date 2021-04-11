from django.urls import path, include

from django.contrib import admin

admin.autodiscover()

from khana.admin import admin_site

import khana.views

from django.contrib.auth import views
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

    path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(template_name='khana/admin/password_reset_confirm_copy.html'), name='password_reset_confirm'),
    path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/login/', khana.views.login_view),
    path('<str:useless>', khana.views.default),
]
