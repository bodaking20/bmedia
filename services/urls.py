from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    path('', views.home, name='home'),
    path('category/<slug:slug>/', views.category_services, name='category_services'), # أضفنا هذا السطر
]