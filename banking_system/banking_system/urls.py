from django.contrib import admin
from django.urls import path
from bs import views
from django.conf.urls import url, include

urlpatterns = [
    # path('', views.login, name='login'),
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    # path('login/', views.login, name='login'),
    url(r'^accounts/', include('django.contrib.auth.urls')),
]