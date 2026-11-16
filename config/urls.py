from django.contrib import admin
from django.urls import path
from studio import views, api

urlpatterns = [
    path("", views.home, name="home"),
    path("services/", views.services, name="services"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("request/", views.request_project, name="request_project"),
    path("privacy/", views.privacy, name="privacy"),
    path("terms/", views.terms, name="terms"),
    path("health/", views.health, name="health"),
    path("api/bot/v1/", api.bot_api, name="bot_api"),
    path("admin/", admin.site.urls),
]
admin.site.site_header = "مدیریت DeltaDevelop"
admin.site.site_title = "پنل دلتا دولوپ"
admin.site.index_title = "مدیریت استودیو توسعه نرم‌افزار"
