from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import MarketerProfile, Referral

@login_required(login_url='accounts:login')
def marketer_dashboard(request):
    # التحقق مما إذا كان المستخدم لديه ملف مسوق
    if hasattr(request.user, 'marketer_account_profile'):
        profile = request.user.marketer_account_profile
        referrals = profile.referrals.all().order_by('-created_at')
        
        # توليد رابط الإحالة الديناميكي بناءً على دومين الموقع
        host = request.get_host()
        referral_link = f"{request.scheme}://{host}/accounts/register/?ref={profile.referral_code}"
        
        context = {
            'is_marketer': True,
            'profile': profile,
            'referrals': referrals,
            'referral_link': referral_link,
        }
    else:
        # إذا لم يكن مسوقاً
        context = {
            'is_marketer': False
        }
        
    return render(request, 'pages/marketer_dashboard.html', context)