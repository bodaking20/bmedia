from django.shortcuts import render, get_object_or_404
from .models import Category, Service

def home(request):
    # جلب جميع الأقسام لعرضها ككروت في الصفحة الرئيسية
    categories = Category.objects.all()
    return render(request, 'pages/home.html', {'categories': categories})

def category_services(request, slug):
    # جلب القسم بناءً على الـ slug، وإذا لم يكن موجوداً يظهر خطأ 404
    category = get_object_or_404(Category, slug=slug)
    # جلب الخدمات التابعة لهذا القسم والتي حالتها "متاحة" فقط
    services = category.services.filter(status='active')
    
    return render(request, 'pages/category_services.html', {
        'category': category,
        'services': services
    })