from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomUserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="البريد الإلكتروني")
    phone = forms.CharField(max_length=20, required=False, label="رقم الهاتف")
    referral_code = forms.CharField(max_length=20, required=False, label="كود إحالة المسوق (إن وجد)", help_text="إذا دعاك مسوق، أدخل كوده هنا.")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'phone', 'referral_code')

    # إضافة كلاسات Bootstrap لجميع الحقول تلقائياً
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
from django.contrib.auth.forms import AuthenticationForm

class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # إضافة كلاس form-control لجميع الحقول (اسم المستخدم وكلمة المرور)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'