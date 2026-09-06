import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('staff', 'Staff'),
        ('marketer', 'Marketer'),
        ('customer', 'Customer'),
    )
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    phone = models.CharField(max_length=20, blank=True, null=True)
    referral_code = models.CharField(max_length=50, unique=True, blank=True, null=True)
    referred_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='referrals')

    def save(self, *args, **kwargs):
        # إنشاء كود إحالة فريد تلقائياً عند التسجيل
        if not self.referral_code:
            self.referral_code = str(uuid.uuid4()).replace('-', '')[:8].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

class MarketerProfile(models.Model):
    COMMISSION_CHOICES = (
        ('percentage', 'Percentage (%)'),
        ('fixed', 'Fixed Amount (EGP)'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='marketer_profile')
    commission_type = models.CharField(max_length=20, choices=COMMISSION_CHOICES, default='percentage')
    commission_value = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    # إحصائيات لوحة تحكم المسوق
    total_sales = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    total_commission = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    available_balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Marketer Profile: {self.user.username}"