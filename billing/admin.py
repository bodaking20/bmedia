from django.contrib import admin
from .models import Wallet, WalletTransaction

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'available_balance', 'pending_balance')
    search_fields = ('user__username', 'user__email')

@admin.register(WalletTransaction)
class WalletTransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'transaction_type', 'amount', 'status', 'created_at')
    list_filter = ('transaction_type', 'status', 'created_at')
    search_fields = ('user__username', 'description')
    list_editable = ('status',) # يتيح لك تغيير الحالة من القائمة الخارجية بسرعة

    def save_model(self, request, obj, form, change):
        # التحقق مما إذا كان هذا تعديلاً على معاملة موجودة (وليس إنشاء واحدة جديدة)
        if change:
            # جلب الحالة القديمة من قاعدة البيانات قبل الحفظ
            old_obj = WalletTransaction.objects.get(pk=obj.pk)
            
            # إذا كانت الحالة القديمة "قيد المراجعة" وتحولت إلى "مقبول" وكان نوعها "إيداع"
            if old_obj.status == 'pending' and obj.status == 'approved' and obj.transaction_type == 'deposit':
                # جلب محفظة العميل وإضافة الرصيد إليها
                wallet = obj.user.wallet
                wallet.available_balance += obj.amount
                wallet.save()
                
        super().save_model(request, obj, form, change)