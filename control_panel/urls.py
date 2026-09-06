from django.urls import path
from . import views

app_name = 'control_panel'

urlpatterns = [
    path('', views.admin_dashboard, name='dashboard'),
    path('deposits/', views.manage_deposits, name='manage_deposits'),
    path('deposits/<int:tx_id>/<str:action>/', views.handle_deposit, name='handle_deposit'),
    path('orders/', views.manage_orders, name='manage_orders'),
    path('orders/<int:order_id>/<str:new_status>/', views.change_order_status, name='change_order_status'),
]