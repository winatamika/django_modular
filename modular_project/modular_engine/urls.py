from django.urls import path
from . import views

urlpatterns = [
    path('', views.module_dashboard, name='home'),
    path('install/<str:name>/', views.install_module, name='install_module'),
    path('uninstall/<str:name>/', views.uninstall_module, name='uninstall_module'),
    path('upgrade/<str:name>/', views.upgrade_module, name='upgrade_module'),
    path('downgrade/<str:name>/', views.downgrade_module, name='downgrade_module'),
]
