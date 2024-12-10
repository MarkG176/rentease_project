"""
URL configuration for rentease_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from main import views


urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('admin/', admin.site.urls),
    path('incidents/', views.incidents_list, name='incidents_list'),

    path('incident/<int:id>/', views.incident_detail, name='incident_detail'),
    
    path('incidents/edit/<int:id>/', views.incident_edit, name='incident_edit'),
    path('incidents/delete/<int:id>/', views.incident_delete, name='incident_delete'),
    path('tenants/', views.tenants_view, name='tenants'),
    # path('charts/delays/', views.delays_chart, name='delays_chart'),
    path('add/tenant', views.add_tenant, name='add_tenant'),
    path('customers/delete/<int:tenant_id>', views.delete_tenant, name='delete_tenant'),
    path('properties/', views.properties_view, name='properties'),

    path('incidents/', views.incidents, name='incidents'),
    path('payments/', views.payments_view, name='payments'),
    path('assign/<int:lot_no>', views.assign_lot, name='assign_lot'),
    #     path('pie-chart', views.pie_chart, name='pie_chart'),
    #     path('line-chart', views.line_chart, name='line_chart'),
    #     path('bar-chart', views.bar_chart, name='bar_chart')
]
