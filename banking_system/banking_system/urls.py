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
    path('replenishment/<int:id>/', views.replenishment, name='replenishment'),
    path('removal/<int:id>/', views.removal, name='removal'),
    path('error_removal/<int:id>/', views.error_removal, name='error_removal'),
    path('monthly_report/', views.monthly_report, name='monthly_report'),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'conversion/', views.conversion, name='conversion'),
]