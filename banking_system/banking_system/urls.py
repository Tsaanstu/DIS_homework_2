from django.contrib import admin
from django.urls import path
from bs import views

urlpatterns = [
    #path('', views.login, name='login'),
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('login/', views.login, name='login'),
]