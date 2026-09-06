from django.db import models
from django.conf import settings
import random
import string

def generate_referral_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

class MarketerProfile(models.Model):
    # أضفنا related_name مميز جداً لمنع أي تعارض
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='marketer_account_profile', verbose_name="المستخدم")
    referral_code = models.CharField(max_length=20, unique=True, default=generate_referral_code, verbose_name="كود الإحالة")
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=5.00, help_text="النسبة المئوية (مثال: 5.00 تعني 5%)", verbose_name="نسبة العمولة (%)")
    is_active = models.BooleanField(default=True, verbose_name="نشط")

    class Meta:
        verbose_name = "ملف مسوق"
        verbose_name_plural = "ملفات المسوقين"

    def __str__(self):
        return f"مسوق: {self.user.username} - {self.referral_code}"

class Referral(models.Model):
    marketer = models.ForeignKey(MarketerProfile, on_delete=models.CASCADE, related_name='referrals', verbose_name="المسوق")
    # غيرنا الـ related_name هنا أيضاً
    referred_user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='invited_by_marketer', verbose_name="العميل المُحال")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ التسجيل")

    class Meta:
        verbose_name = "إحالة"
        verbose_name_plural = "سجل الإحالات"

    def __str__(self):
        return f"{self.referred_user.username} سجل عن طريق {self.marketer.user.username}"