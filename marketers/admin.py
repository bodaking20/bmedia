from django.contrib import admin
from .models import MarketerProfile, Referral

@admin.register(MarketerProfile)
class MarketerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'referral_code', 'commission_rate', 'is_active')
    search_fields = ('user__username', 'referral_code')
    list_editable = ('commission_rate', 'is_active') # لتعديل نسبة العمولة بسرعة

@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    list_display = ('referred_user', 'marketer', 'created_at')
    search_fields = ('referred_user__username', 'marketer__referral_code')
    readonly_fields = ('created_at',)