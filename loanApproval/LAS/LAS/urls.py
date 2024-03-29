"""LAS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf.urls import url
from loans import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


# urlpatterns = [
#     path('accounts/', include('django.contrib.auth.urls')),
#     path('accounts/signup/admin/', views.BankAdminSignUpView.as_view(), name='admin_signup'),
#     path('accounts/signup/customer/', views.CustomerSignUpView.as_view(), name='customer_signup'),
#     path('loans/', include('loans.urls')),
#     path('admin/', admin.site.urls),
    # url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    # url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    # url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #     auth_views.password_reset_confirm, name='password_reset_confirm'),
    # url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
# ]

# url(r'^reset_password_confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', views.PasswordResetConfirmView.as_view(),name='reset_password_confirm'),

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    url(r'^$',views.index,name='index'),
    url(r'^special/',views.special,name='special'),
    url(r'^loans/',include('loans.urls')),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^register/$',views.register,name='register'),
    # url(r'^admin_login/$',views.admin_login,name='admin_login'),
    url(r'^user_login/$',views.user_login,name='user_login'),
    url(r'^change_password/$',views.change_password,name='change_password'),
    url(r'^edit_profile/$',views.edit_profile,name='edit_profile'),
    url(r'^reset_password/$',views.reset_password,name='reset_password'),
    url(r'^reset_password_confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',views.confirm,name='reset_password_confirm'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)