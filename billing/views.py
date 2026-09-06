from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import WalletTransaction, Wallet

@login_required(login_url='accounts:login')
def add_balance(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        payment_method = request.POST.get('payment_method')
        transfer_number = request.POST.get('transfer_number')
        
        # التأكد من أن المبلغ صحيح
        if not amount or float(amount) <= 0:
            messages.error(request, 'يرجى إدخال مبلغ صحيح أكبر من الصفر.')
            return redirect('billing:add_balance')
            
        # دمج التفاصيل في حقل الوصف ليراها الأدمن
        description = f"طريقة الدفع: {payment_method} | رقم التحويل: {transfer_number}"
        
        # إنشاء حركة مالية جديدة بحالة "قيد المراجعة"
        WalletTransaction.objects.create(
            user=request.user,
            amount=amount,
            transaction_type='deposit',
            status='pending',
            description=description
        )
        
        messages.success(request, 'تم إرسال طلب الشحن بنجاح! سيتم إضافة الرصيد لمحفظتك فور مراجعته من الإدارة.')
        return redirect('accounts:dashboard')
        
    return render(request, 'pages/add_balance.html')