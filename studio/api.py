"""Minimal authenticated admin bot API. No commerce or fake invoices."""
import json
import os
import secrets
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import ProjectRequest, Service, StudioProfile

CAPABILITIES = ["studio_dashboard", "studio_services", "studio_requests", "studio_profile"]


def result(data=None, **extra):
    return JsonResponse({"ok": True, "data": data, **extra})


def error(reason, status=400):
    return JsonResponse({"ok": False, "error": reason}, status=status)


def authorized(request):
    expected = os.getenv("DELTADEVELOP_BOT_API_KEY", "")
    supplied = request.headers.get("Authorization", "")
    return (
        len(expected) >= 32 and supplied.startswith("Bearer ")
        and secrets.compare_digest(supplied[7:], expected)
    )


@csrf_exempt
def bot_api(request):
    if request.method != "POST":
        return error("POST required", 405)
    if not authorized(request):
        return error("unauthorized", 401)
    if len(request.body) > 32768:
        return error("request_too_large", 413)
    try:
        data = json.loads(request.body or "{}")
    except (ValueError, UnicodeError):
        return error("invalid_json")
    if not isinstance(data, dict):
        return error("invalid_payload")
    action = data.get("action")
    payload = data.get("payload") or {}
    if not isinstance(payload, dict):
        return error("invalid_payload")

    if action == "ping":
        profile = StudioProfile.load()
        return result(None, site={
            "name": profile.name, "platform": "deltadevelop",
            "version": 1, "domain": "deltadevelop.ir",
            "capabilities": CAPABILITIES,
        })
    # The shared Telegram notification poller queries every connected site.
    # This brochure site has no event queue yet; return an honest empty feed.
    if action == "events_poll":
        return result([])
    if action == "events_ack":
        return result({"acknowledged": 0})
    if action == "dashboard":
        return result({
            "service_count": Service.objects.filter(is_active=True).count(),
            "new_requests": ProjectRequest.objects.filter(status="new").count(),
            "total_requests": ProjectRequest.objects.count(),
        })
    if action == "settings_get":
        profile = StudioProfile.load()
        return result({
            "name": profile.name, "slogan": profile.slogan,
            "email": profile.email, "phone": profile.phone,
            "address": profile.address,
        })
    if action == "services_list":
        return result([{
            "id": item.pk, "title": item.title,
            "is_active": item.is_active, "order": item.order,
        } for item in Service.objects.order_by("order", "pk")[:100]])
    if action == "service_toggle":
        try:
            pk = int(payload.get("id"))
        except (TypeError, ValueError):
            return error("invalid_id")
        item = Service.objects.filter(pk=pk).first()
        if not item:
            return error("service_not_found", 404)
        item.is_active = not item.is_active
        item.save(update_fields=["is_active"])
        return result({"id": item.pk, "is_active": item.is_active})
    if action == "requests_list":
        return result([{
            "id": item.pk, "name": item.name, "service": item.service.title if item.service else "عمومی",
            "status": item.status, "date": item.created_at.isoformat(),
        } for item in ProjectRequest.objects.select_related("service")[:30]])
    if action == "request_detail":
        try:
            pk = int(payload.get("id"))
        except (TypeError, ValueError):
            return error("invalid_id")
        item = ProjectRequest.objects.select_related("service").filter(pk=pk).first()
        if not item:
            return error("request_not_found", 404)
        return result({
            "id": item.pk, "name": item.name, "email": item.email,
            "phone": item.phone, "description": item.description,
            "service": item.service.title if item.service else "عمومی",
            "status": item.status, "date": item.created_at.isoformat(),
        })
    if action == "request_status":
        try:
            pk = int(payload.get("id"))
        except (TypeError, ValueError):
            return error("invalid_id")
        status = str(payload.get("status") or "")
        if status not in {v for v, _ in ProjectRequest.STATUS}:
            return error("invalid_status")
        changed = ProjectRequest.objects.filter(pk=pk).update(status=status)
        if not changed:
            return error("request_not_found", 404)
        return result({"id": pk, "status": status})
    return error("unknown_action", 400)
