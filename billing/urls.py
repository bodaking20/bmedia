from django.urls import path
from . import views

app_name = 'billing'

urlpatterns = [
    path('add/', views.add_balance, name='add_balance'),
]