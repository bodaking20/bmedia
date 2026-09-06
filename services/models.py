from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="اسم القسم")
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True, null=True, verbose_name="وصف القسم")
    icon = models.ImageField(upload_to='categories/icons/', blank=True, null=True, verbose_name="أيقونة القسم")
    
    class Meta:
        verbose_name = "قسم"
        verbose_name_plural = "الأقسام"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Service(models.Model):
    STATUS_CHOICES = (
        ('active', 'متاحة'),
        ('inactive', 'غير متاحة'),
    )

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='services', verbose_name="القسم")
    name = models.CharField(max_length=255, verbose_name="اسم الخدمة")
    description = models.TextField(blank=True, null=True, verbose_name="وصف الخدمة")
    
    # تفاصيل الأسعار
    provider_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="تكلفة المزود")
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="السعر الذي يظهر للعميل (سعر البيع)", verbose_name="السعر للعميل")
    
    # تفاصيل الكميات
    base_quantity = models.PositiveIntegerField(default=1000, help_text="مثال: السعر أعلاه لكل 1000 وحدة", verbose_name="الكمية الأساسية")
    min_quantity = models.PositiveIntegerField(default=10, verbose_name="الحد الأدنى للطلب")
    max_quantity = models.PositiveIntegerField(default=100000, verbose_name="الحد الأقصى للطلب")
    
    # ربط الـ API مستقبلاً
    provider_service_id = models.CharField(max_length=100, blank=True, null=True, help_text="ID الخدمة في موقع المزود (للربط التلقائي)", verbose_name="Provider Service ID")
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', verbose_name="حالة الخدمة")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "خدمة"
        verbose_name_plural = "الخدمات"

    def __str__(self):
        return f"{self.name} - {self.category.name}"