# DeltaDevelop — استودیو توسعه نرم‌افزار

**دامنه:** https://deltadevelop.ir  
**ریپو:** `deltashopsiavash/deltadevelop`

پروژه مستقل از SanaShop و DeltaJanebi، با پنل Django، معرفی خدمات و ثبت درخواست واقعی پروژه. **فروشگاه، فاکتور یا پرداخت در نسخه ۱ وجود ندارد.**

## قابلیت‌ها

- سایت فارسی RTL، موبایل‌فرندلی: خانه، خدمات، درباره ما، تماس، ثبت درخواست، حریم خصوصی، شرایط خدمات
- پنل مدیریت `/admin/`: ویرایش هویت واقعی کسب‌وکار، خدمات و درخواست‌ها
- فرم درخواست پروژه با CSRF، رضایت کاربر و کنترل ضداسپم ساده
- API ربات مستقل `POST /api/bot/v1/` با کلید جداگانه `DELTADEVELOP_BOT_API_KEY`
- `ping` با `platform=deltadevelop`، آمار، فهرست/فعال‌سازی خدمات، فهرست و وضعیت درخواست‌ها
- بدون دسترسی به دیتابیس‌ها و کلیدهای SanaShop/DeltaJanebi

## اجرای محلی

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export DJANGO_DEBUG=1
export DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
export DELTADEVELOP_BOT_API_KEY="$(python -c 'import secrets;print(secrets.token_urlsafe(48))')"
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

سپس `http://127.0.0.1:8000/` و `http://127.0.0.1:8000/admin/` را باز کن.

## راه‌اندازی روی VPS

برای سرور مستقل، PostgreSQL و Gunicorn و Caddy استفاده کن (نمونه فایل‌ها در `deploy/`). تنظیمات حتماً در `/etc/deltadevelop/site.env` با دسترسی `0600` باشند و داخل GitHub بارگذاری نشوند. 
- `DJANGO_DEBUG=0`
- `DJANGO_SECRET_KEY`: مقدار تصادفی حداقل ۵۰ نویسه
- `DELTADEVELOP_BOT_API_KEY`: کلید تصادفی مستقل حداقل ۳۲ نویسه، فقط نزد مدیر سایت و اتصال ربات
- `DATABASE_URL`: اتصال PostgreSQL اختصاصی DeltaDevelop
- `DJANGO_ALLOWED_HOSTS=deltadevelop.ir,www.deltadevelop.ir`
- `DJANGO_CSRF_TRUSTED_ORIGINS=https://deltadevelop.ir,https://www.deltadevelop.ir`
- پس از فعال شدن TLS، `DJANGO_SECURE_SSL_REDIRECT=1`

```bash
python manage.py migrate --noinput
python manage.py collectstatic --noinput
python manage.py check --deploy
```

توجه: نمونه‌های systemd و Caddy باید پیش از نصب با شرایط واقعی VPS هماهنگ شوند؛ این نسخه هنوز روی VPS اجرا نشده است.

## اتصال ربات مشترک ger1

سایت بعد از نصب با توکن مخصوص خودش پاسخ API می‌دهد. ماژول روتر ربات مشترک باید پلتفرم سوم `deltadevelop` را به رسمیت بشناسد تا از پنل SanaShop یا DeltaJanebi استفاده نکند. در ربات از **اتصال سایت جدید** استفاده کن و آدرس `https://deltadevelop.ir` و کلید تولیدشده همان سایت را وارد کن.

کلید در پاسخ `ping` بازگردانده نمی‌شود؛ فقط از مسیر خصوصی نصب دریافت شود.

## آماده‌سازی برای اینماد

اطلاعات واقعی مالک کسب‌وکار، آدرس، شماره تماس، شرح خدمات و شرایط همکاری باید **قبل از ارسال برای بررسی نماد** تکمیل شوند. فعلاً نمونه‌کار یا سابقه مشتری ساختگی نمایش داده نمی‌شود. دریافت اینماد به ارزیابی مرجع مربوط بستگی دارد، نه صرفاً داشتن ظاهر حرفه‌ای سایت.
