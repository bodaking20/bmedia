from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required 
# تم استدعاء CustomLoginForm هنا
from .forms import CustomUserRegistrationForm, CustomLoginForm

from orders.models import Order
from billing.models import Wallet
from marketers.models import MarketerProfile, Referral # استدعاء نماذج التسويق

def register_view(request):
    if request.user.is_authenticated:
        return redirect('services:home')
        
    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # 1. إنشاء محفظة للعميل الجديد تلقائياً
            Wallet.objects.get_or_create(user=user)

            # 2. نظام ربط الإحالة (Referral Logic)
            referral_code = form.cleaned_data.get('referral_code')
            if referral_code:
                try:
                    # البحث عن المسوق صاحب هذا الكود
                    marketer = MarketerProfile.objects.get(referral_code=referral_code, is_active=True)
                    # ربط العميل الجديد بالمسوق
                    Referral.objects.create(marketer=marketer, referred_user=user)
                except MarketerProfile.DoesNotExist:
                    # إذا كان الكود غير صحيح، نتجاهله ويتم تسجيل العميل بشكل طبيعي
                    pass
            
            login(request, user)
            messages.success(request, f'تم إنشاء الحساب بنجاح، مرحباً بك يا {user.username}!')
            return redirect('services:home')
    else:
        # الميزة الذكية: قراءة الكود من الرابط تلقائياً إذا كان موجوداً
        initial_code = request.GET.get('ref', '')
        form = CustomUserRegistrationForm(initial={'referral_code': initial_code})
    
    return render(request, 'pages/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('services:home')

    if request.method == 'POST':
        # استخدام النموذج المخصص هنا
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'تم تسجيل الدخول بنجاح.')
                return redirect('services:home')
    else:
        # استخدام النموذج المخصص هنا أيضاً
        form = CustomLoginForm()
        
    return render(request, 'pages/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'تم تسجيل الخروج بنجاح.')
    return redirect('services:home')

@login_required(login_url='accounts:login')
def dashboard_view(request):
    wallet, created = Wallet.objects.get_or_create(user=request.user)
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'wallet': wallet,
        'orders': orders,
    }
    return render(request, 'pages/dashboard.html', context)