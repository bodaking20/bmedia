import decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from services.models import Service
from .models import Order
from billing.models import Wallet, WalletTransaction
from marketers.models import Referral # استدعاء نموذج الإحالة

@login_required(login_url='accounts:login')
def create_order(request, service_id):
    service = get_object_or_404(Service, id=service_id, status='active')
    
    # التأكد من وجود محفظة للمستخدم (وإنشائها إن لم تكن موجودة)
    wallet, created = Wallet.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        link = request.POST.get('link')
        quantity = int(request.POST.get('quantity', 0))
        notes = request.POST.get('notes', '')
        
        # التحقق من الكمية
        if quantity < service.min_quantity or quantity > service.max_quantity:
            messages.error(request, 'الكمية المطلوبة غير مسموح بها لهذه الخدمة.')
            return redirect('orders:create_order', service_id=service.id)
        
        # حساب التكلفة الإجمالية برمجياً (حماية من التلاعب)
        total_price = (decimal.Decimal(quantity) / decimal.Decimal(service.base_quantity)) * service.price
        
        # التحقق من الرصيد
        if wallet.available_balance < total_price:
            messages.error(request, 'رصيدك غير كافٍ لإتمام هذا الطلب. يرجى شحن محفظتك.')
            return redirect('orders:create_order', service_id=service.id)
        
        # 1. خصم الرصيد من العميل
        wallet.available_balance -= total_price
        wallet.save()
        
        # 2. إنشاء الطلب للعميل
        order = Order.objects.create(
            user=request.user,
            service=service,
            link=link,
            quantity=quantity,
            total_price=total_price,
            notes=notes
        )
        
        # 3. تسجيل حركة الخصم للعميل
        WalletTransaction.objects.create(
            user=request.user,
            amount=total_price,
            transaction_type='purchase',
            status='approved',
            description=f'خصم لطلب خدمة: {service.name} (طلب #{order.id})'
        )

        # ---------------------------------------------------------
        # 4. السحر: نظام العمولة التلقائي للمسوق (Auto-Commission)
        # ---------------------------------------------------------
        if hasattr(request.user, 'invited_by_marketer'):
            referral = request.user.invited_by_marketer
            marketer = referral.marketer
            
            # التأكد أن حساب المسوق نشط
            if marketer.is_active:
                # حساب مبلغ العمولة بدقة
                commission_amount = total_price * (marketer.commission_rate / decimal.Decimal('100.0'))
                
                if commission_amount > 0:
                    # جلب محفظة المسوق
                    marketer_wallet, _ = Wallet.objects.get_or_create(user=marketer.user)
                    
                    # إضافة الأرباح لمحفظة المسوق
                    marketer_wallet.available_balance += commission_amount
                    marketer_wallet.save()
                    
                    # تسجيل حركة مالية للمسوق (أرباح تسويق)
                    WalletTransaction.objects.create(
                        user=marketer.user,
                        amount=commission_amount,
                        transaction_type='deposit',
                        status='approved',
                        description=f'أرباح تسويق عمولة ({marketer.commission_rate}%) من طلب العميل {request.user.username}'
                    )
        
        messages.success(request, 'تم استلام طلبك بنجاح وجاري التنفيذ!')
        return redirect('services:home')
        
    return render(request, 'pages/order_form.html', {'service': service, 'wallet': wallet})