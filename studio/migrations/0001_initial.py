from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="StudioProfile",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(default="DeltaDevelop", max_length=100, verbose_name="نام برند")),
                ("slogan", models.CharField(default="از ایده تا محصول نرم‌افزاری", max_length=180, verbose_name="شعار")),
                ("introduction", models.TextField(blank=True, verbose_name="معرفی کوتاه")),
                ("about", models.TextField(blank=True, verbose_name="درباره مجموعه")),
                ("email", models.EmailField(blank=True, max_length=254, verbose_name="ایمیل تماس")),
                ("phone", models.CharField(blank=True, max_length=40, verbose_name="تلفن تماس")),
                ("address", models.CharField(blank=True, max_length=350, verbose_name="نشانی واقعی")),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={"verbose_name": "هویت کسب‌وکار", "verbose_name_plural": "هویت کسب‌وکار"},
        ),
        migrations.CreateModel(
            name="Service",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False, verbose_name="ID")),
                ("slug", models.SlugField(allow_unicode=True, max_length=70, unique=True, verbose_name="شناسه لینک")),
                ("title", models.CharField(max_length=130, verbose_name="عنوان خدمت")),
                ("short_description", models.CharField(max_length=280, verbose_name="خلاصه")),
                ("description", models.TextField(blank=True, verbose_name="توضیحات")),
                ("order", models.PositiveSmallIntegerField(default=10, verbose_name="ترتیب")),
                ("is_active", models.BooleanField(default=True, verbose_name="نمایش در سایت")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "ordering": ("order", "id"), "verbose_name": "خدمت نرم‌افزاری",
                "verbose_name_plural": "خدمات نرم‌افزاری",
            },
        ),
        migrations.CreateModel(
            name="ProjectRequest",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=130, verbose_name="نام درخواست‌دهنده")),
                ("email", models.EmailField(max_length=254, verbose_name="ایمیل")),
                ("phone", models.CharField(blank=True, max_length=40, verbose_name="شماره تماس")),
                ("description", models.TextField(max_length=4000, verbose_name="توضیحات پروژه")),
                ("status", models.CharField(choices=[("new", "جدید"), ("reviewing", "در حال بررسی"), ("contacted", "تماس گرفته شد"), ("closed", "بسته‌شده")], default="new", max_length=20, verbose_name="وضعیت")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت")),
                ("service", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="requests", to="studio.service", verbose_name="خدمت")),
            ],
            options={"ordering": ("-created_at",), "verbose_name": "درخواست پروژه", "verbose_name_plural": "درخواست‌های پروژه"},
        ),
    ]
