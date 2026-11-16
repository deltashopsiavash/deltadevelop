import json
from django.test import TestCase, override_settings
from django.urls import reverse
from .models import ProjectRequest, Service, StudioProfile

API = "/api/bot/v1/"
KEY = "development-test-key-longer-than-32-characters"


class PublicSiteTests(TestCase):
    def test_home_and_pages(self):
        for page in ("home", "services", "about", "contact", "privacy", "terms", "request_project"):
            self.assertEqual(self.client.get(reverse(page)).status_code, 200)
        self.assertContains(self.client.get("/"), "DeltaDevelop")
        self.assertNotContains(self.client.get("/"), "مشتری راضی")

    def test_actual_request_can_be_registered(self):
        item = Service.objects.create(slug="bot", title="ربات", short_description="طراحی ربات")
        response = self.client.post("/request/", {
            "name": "مشتری آزمون", "email": "real.user@example.com",
            "phone": "09120000000", "service": item.pk,
            "description": "برای یک سامانه واقعی نیاز به پنل مدیریت دارم.",
            "accept_privacy": "on",
            "website": "",
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ProjectRequest.objects.count(), 1)

    def test_honeypot_refuses_bot_submission(self):
        response = self.client.post("/request/", {
            "name": "test", "email": "x@example.com", "description": "test",
            "accept_privacy": "on", "website": "spam.example",
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ProjectRequest.objects.count(), 0)


class BotApiTests(TestCase):
    def setUp(self):
        import os
        self._old = os.environ.get("DELTADEVELOP_BOT_API_KEY")
        os.environ["DELTADEVELOP_BOT_API_KEY"] = KEY
        self.addCleanup(self.restore_key)

    def restore_key(self):
        import os
        if self._old is None:
            os.environ.pop("DELTADEVELOP_BOT_API_KEY", None)
        else:
            os.environ["DELTADEVELOP_BOT_API_KEY"] = self._old

    def post(self, action, payload=None, token=KEY):
        return self.client.post(API, data=json.dumps({"action": action, "payload": payload or {}}),
            content_type="application/json", HTTP_AUTHORIZATION="Bearer " + token)

    def test_api_requires_secret(self):
        self.assertEqual(self.post("ping", token="wrong").status_code, 401)
        self.assertEqual(self.client.get(API).status_code, 405)

    def test_ping_is_distinct_platform(self):
        body = self.post("ping").json()
        self.assertEqual(body["site"]["platform"], "deltadevelop")
        self.assertIn("studio_dashboard", body["site"]["capabilities"])

    def test_services_and_inquiries_are_separated(self):
        service = Service.objects.create(slug="site", title="طراحی سایت", short_description="سایت شرکتی")
        ProjectRequest.objects.create(name="A", email="a@example.com", description="Design", service=service)
        self.assertEqual(self.post("dashboard").json()["data"]["total_requests"], 1)
        self.assertEqual(self.post("services_list").json()["data"][0]["title"], "طراحی سایت")
        self.assertEqual(self.post("requests_list").json()["data"][0]["name"], "A")
        self.assertTrue(self.post("service_toggle", {"id": service.id}).json()["ok"])
        self.assertFalse(Service.objects.get(pk=service.pk).is_active)
        self.assertTrue(self.post("request_status", {"id": 1, "status": "reviewing"}).json()["ok"])
        self.assertEqual(ProjectRequest.objects.get(pk=1).status, "reviewing")

    def test_no_fake_payment_api(self):
        self.assertEqual(self.post("create_invoice", {"amount": 80000}).status_code, 400)
