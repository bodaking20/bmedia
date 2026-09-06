from django.urls import path
from . import views

app_name = 'marketers'

urlpatterns = [
    path('dashboard/', views.marketer_dashboard, name='dashboard'),
]