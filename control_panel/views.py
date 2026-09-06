from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import get_user_model
from django.contrib import messages

from orders.models import Order
from billing.models import WalletTransaction

User = get_user_model()

# دالة حماية: للتأكد أن المستخدم هو أدمن أو ضمن فريق العمل
def is_admin(user):
    return user.is_staff or user.is_superuser

@user_passes_test(is_admin, login_url='services:home')
def admin_dashboard(request):
    # جلب الإحصائيات السريعة
    total_users = User.objects.count()
    pending_orders = Order.objects.filter(status='pending').count()
    pending_deposits = WalletTransaction.objects.filter(transaction_type='deposit', status='pending').count()
    completed_orders = Order.objects.filter(status='completed').count()
    
    # جلب أحدث الطلبات المعلقة لعرضها في الرئيسية
    recent_orders = Order.objects.filter(status='pending').order_by('-created_at')[:5]
    
    context = {
        'total_users': total_users,
        'pending_orders': pending_orders,
        'pending_deposits': pending_deposits,
        'completed_orders': completed_orders,
        'recent_orders': recent_orders,
    }
    return render(request, 'pages/control_panel/dashboard.html', context)

@user_passes_test(is_admin, login_url='services:home')
def manage_deposits(request):
    # جلب كل طلبات الشحن المعلقة
    pending_deposits = WalletTransaction.objects.filter(transaction_type='deposit', status='pending').order_by('-created_at')
    
    context = {
        'deposits': pending_deposits
    }
    return render(request, 'pages/control_panel/deposits.html', context)

@user_passes_test(is_admin, login_url='services:home')
def handle_deposit(request, tx_id, action):
    # جلب المعاملة
    tx = get_object_or_404(WalletTransaction, id=tx_id)
    
    if tx.status == 'pending':
        if action == 'approve':
            tx.status = 'approved'
            tx.save()
            
            # إضافة الرصيد لمحفظة العميل
            wallet = tx.user.wallet
            wallet.available_balance += tx.amount
            wallet.save()
            messages.success(request, f'تم الموافقة على شحن {tx.amount} جنيه للعميل {tx.user.username} بنجاح!')
            
        elif action == 'reject':
            tx.status = 'rejected'
            tx.save()
            messages.info(request, f'تم رفض طلب الشحن للعميل {tx.user.username}.')
            
    return redirect('control_panel:manage_deposits')

@user_passes_test(is_admin, login_url='services:home')
def manage_orders(request):
    # جلب الطلبات النشطة (التي تحتاج عمل)
    active_orders = Order.objects.exclude(status__in=['completed', 'cancelled']).order_by('-created_at')
    
    context = {
        'orders': active_orders
    }
    return render(request, 'pages/control_panel/orders.html', context)

@user_passes_test(is_admin, login_url='services:home')
def change_order_status(request, order_id, new_status):
    order = get_object_or_404(Order, id=order_id)
    valid_statuses = ['pending', 'processing', 'completed', 'cancelled']
    
    if new_status in valid_statuses and order.status != new_status:
        # نظام استرداد الأموال (Refund) في حالة الإلغاء
        if new_status == 'cancelled' and order.status != 'cancelled':
            wallet = order.user.wallet
            wallet.available_balance += order.total_price
            wallet.save()
            
            # تسجيل حركة الاسترداد
            WalletTransaction.objects.create(
                user=order.user,
                amount=order.total_price,
                transaction_type='deposit',
                status='approved',
                description=f'استرداد رصيد لإلغاء طلب (رقم #{order.id})'
            )
            messages.warning(request, f'تم إلغاء الطلب #{order.id} واسترداد {order.total_price} جنيه لمحفظة العميل.')
            
        elif new_status == 'completed':
            messages.success(request, f'تم إنجاز الطلب #{order.id} بنجاح!')
        else:
            messages.info(request, f'تم تغيير حالة الطلب #{order.id} بنجاح.')
            
        # تحديث حالة الطلب
        order.status = new_status
        order.save()
        
    return redirect('control_panel:manage_orders')