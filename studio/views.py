from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from .forms import ProjectRequestForm
from .models import Service, StudioProfile


def home(request):
    return render(request, "studio/home.html", {
        "services": list(Service.objects.filter(is_active=True)[:6]),
    })


def services(request):
    return render(request, "studio/services.html", {
        "services": Service.objects.filter(is_active=True),
    })


def about(request):
    return render(request, "studio/info.html", {"page": "about"})


def contact(request):
    return render(request, "studio/info.html", {"page": "contact"})


def privacy(request):
    return render(request, "studio/info.html", {"page": "privacy"})


def terms(request):
    return render(request, "studio/info.html", {"page": "terms"})


@require_http_methods(["GET", "POST"])
def request_project(request):
    if request.method == "POST":
        form = ProjectRequestForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "درخواست ثبت شد. پس از بررسی، از طریق اطلاعات ثبت‌شده با شما تماس گرفته می‌شود.")
            return redirect("request_project")
    else:
        form = ProjectRequestForm(initial={"service": request.GET.get("service")})
    return render(request, "studio/request.html", {"form": form})


def health(request):
    return JsonResponse({"ok": True, "service": "deltadevelop"})
