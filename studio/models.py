from django.db import models


class StudioProfile(models.Model):
    """Real editable identity: no fabricated contact details or credentials."""
    name = models.CharField("نام برند", max_length=100, default="DeltaDevelop")
    slogan = models.CharField("شعار", max_length=180, default="از ایده تا محصول نرم‌افزاری")
    introduction = models.TextField("معرفی کوتاه", blank=True)
    about = models.TextField("درباره مجموعه", blank=True)
    email = models.EmailField("ایمیل تماس", blank=True)
    phone = models.CharField("تلفن تماس", max_length=40, blank=True)
    address = models.CharField("نشانی واقعی", max_length=350, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "هویت کسب‌وکار"
        verbose_name_plural = "هویت کسب‌وکار"

    @classmethod
    def load(cls):
        return cls.objects.get_or_create(pk=1)[0]

    def __str__(self):
        return self.name


class Service(models.Model):
    slug = models.SlugField("شناسه لینک", max_length=70, unique=True, allow_unicode=True)
    title = models.CharField("عنوان خدمت", max_length=130)
    short_description = models.CharField("خلاصه", max_length=280)
    description = models.TextField("توضیحات", blank=True)
    order = models.PositiveSmallIntegerField("ترتیب", default=10)
    is_active = models.BooleanField("نمایش در سایت", default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("order", "id")
        verbose_name = "خدمت نرم‌افزاری"
        verbose_name_plural = "خدمات نرم‌افزاری"

    def __str__(self):
        return self.title


class ProjectRequest(models.Model):
    STATUS = [
        ("new", "جدید"), ("reviewing", "در حال بررسی"),
        ("contacted", "تماس گرفته شد"), ("closed", "بسته‌شده"),
    ]
    name = models.CharField("نام درخواست‌دهنده", max_length=130)
    email = models.EmailField("ایمیل")
    phone = models.CharField("شماره تماس", max_length=40, blank=True)
    service = models.ForeignKey(
        Service, verbose_name="خدمت", on_delete=models.SET_NULL,
        null=True, blank=True, related_name="requests",
    )
    description = models.TextField("توضیحات پروژه", max_length=4000)
    status = models.CharField("وضعیت", max_length=20, choices=STATUS, default="new")
    created_at = models.DateTimeField("تاریخ ثبت", auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "درخواست پروژه"
        verbose_name_plural = "درخواست‌های پروژه"

    def __str__(self):
        return f"{self.name} — {self.get_status_display()}"
