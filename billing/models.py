from django.db import models
from django.conf import settings

class Wallet(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wallet', verbose_name="المستخدم")
    available_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name="الرصيد المتاح")
    pending_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name="الرصيد المعلق")

    class Meta:
        verbose_name = "محفظة"
        verbose_name_plural = "المحافظ"

    def __str__(self):
        return f"محفظة {self.user.username} - {self.available_balance} جنيه"

class WalletTransaction(models.Model):
    TRANSACTION_TYPES = (
        ('deposit', 'إيداع / شحن رصيد'),
        ('purchase', 'خصم / شراء خدمة'),
        ('commission', 'إضافة عمولة تسويق'),
        ('refund', 'استرجاع رصيد'),
    )
    
    STATUS_CHOICES = (
        ('pending', 'قيد المراجعة'),
        ('approved', 'مقبول / مكتمل'),
        ('rejected', 'مرفوض'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='transactions', verbose_name="المستخدم")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="المبلغ")
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES, verbose_name="نوع المعاملة")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="حالة المعاملة")
    description = models.TextField(blank=True, null=True, verbose_name="تفاصيل / ملاحظات")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ المعاملة")

    class Meta:
        verbose_name = "حركة مالية"
        verbose_name_plural = "سجل الحركات المالية"

    def __str__(self):
        return f"{self.get_transaction_type_display()} - {self.user.username} ({self.amount})"