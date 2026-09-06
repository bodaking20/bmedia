from django.db import models
from django.conf import settings
from services.models import Service

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'قيد الانتظار'),
        ('processing', 'جاري التنفيذ'),
        ('in_progress', 'قيد العمل'),
        ('completed', 'مكتمل'),
        ('partial', 'مكتمل جزئياً'),
        ('cancelled', 'ملغى'),
        ('refunded', 'مسترجع'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders', verbose_name="العميل/المسوق")
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, related_name='orders', verbose_name="الخدمة")
    
    # تفاصيل الطلب
    link = models.CharField(max_length=500, verbose_name="الرابط (Link)")
    quantity = models.PositiveIntegerField(verbose_name="العدد المطلوب")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="إجمالي التكلفة")
    notes = models.TextField(blank=True, null=True, verbose_name="ملاحظات إضافية")
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="حالة الطلب")
    
    # حقل الربط مع مزودي الخدمة (Providers API) مستقبلاً
    provider_order_id = models.CharField(max_length=100, blank=True, null=True, verbose_name="رقم طلب المزود (API ID)")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الطلب")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="آخر تحديث")

    class Meta:
        verbose_name = "طلب"
        verbose_name_plural = "الطلبات"
        ordering = ['-created_at'] # ترتيب الطلبات من الأحدث للأقدم

    def __str__(self):
        service_name = self.service.name if self.service else 'خدمة محذوفة'
        return f"طلب #{self.id} - {service_name} ({self.user.username})"