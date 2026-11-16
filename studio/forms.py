from django import forms
from .models import ProjectRequest


class ProjectRequestForm(forms.ModelForm):
    accept_privacy = forms.BooleanField(
        label="با ثبت و پردازش اطلاعات برای پاسخ‌گویی به درخواست موافقم.",
        required=True,
    )
    website = forms.CharField(required=False, widget=forms.HiddenInput)

    class Meta:
        model = ProjectRequest
        fields = ("name", "email", "phone", "service", "description")
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "نام و نام خانوادگی"}),
            "email": forms.EmailInput(attrs={"placeholder": "example@email.com"}),
            "phone": forms.TextInput(attrs={"placeholder": "اختیاری"}),
            "description": forms.Textarea(attrs={"rows": 5, "placeholder": "درباره ایده، نیازمندی‌ها و زمان‌بندی دلخواه بنویسید..."}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["service"].queryset = self.fields["service"].queryset.filter(is_active=True)
        self.fields["service"].required = False
        self.fields["service"].empty_label = "مشاوره عمومی"

    def clean_website(self):
        if self.cleaned_data.get("website"):
            raise forms.ValidationError("درخواست قابل پردازش نیست.")
        return ""
