from django.contrib import admin
from django.urls import path
from bs import views
from django.conf.urls import url, include

urlpatterns = [
    # path('', views.login, name='login'),
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('client_data/<int:id>/', views.client_data, name='client_data'),
    path('transfer/<int:id>/', views.transfer, name='transfer'),
    path('report/<int:id>/', views.report, name='report'),
    url(r'^accounts/', include('django.contrib.auth.urls')),
]