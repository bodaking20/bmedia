from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('create/<int:service_id>/', views.create_order, name='create_order'),
]