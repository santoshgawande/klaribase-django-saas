from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.core.management import call_command
from django.test import Client, TestCase
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from session_security.utils import get_last_activity, set_last_activity

User = get_user_model()


class SessionSecurityAdminTests(TestCase):
    def setUp(self):
        self.staff_user = User.objects.create_user(
            email="staff@klaribase.com",
            username="staff_user",
            password="StrongPassword123!",
            is_staff=True,
            is_superuser=True,
        )
        self.regular_user = User.objects.create_user(
            email="member@klaribase.com",
            username="member_user",
            password="MemberPassword123!",
            is_staff=False,
        )
        self.client = Client()

    def test_ac1_idle_staff_user_is_logged_out(self):
        """AC1: Logged-in staff whose last activity is older than EXPIRE_AFTER gets logged out on next request."""
        self.client.force_login(self.staff_user)

        # Pre-condition: user is logged in
        session = self.client.session
        self.assertEqual(session.get("_auth_user_id"), str(self.staff_user.pk))

        # Simulate inactivity beyond EXPIRE_AFTER (e.g. 700 seconds ago when default is 600)
        old_activity = datetime.now() - timedelta(seconds=700)
        set_last_activity(session, old_activity)
        session.save()

        # Next admin request must trigger logout and redirect to login
        response = self.client.get(reverse("admin:index"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("admin:login"), response.url)

        # Assert server-side logout: _auth_user_id is gone
        refreshed_session = self.client.session
        self.assertNotIn("_auth_user_id", refreshed_session)

    def test_ac2_active_staff_user_stays_logged_in_and_refreshes_activity(self):
        """AC2: Staff user active within EXPIRE_AFTER stays logged in, and request refreshes their last activity."""
        self.client.force_login(self.staff_user)

        # Simulate recent activity (100 seconds ago)
        recent_activity = datetime.now() - timedelta(seconds=100)
        session = self.client.session
        set_last_activity(session, recent_activity)
        session.save()

        response = self.client.get(reverse("admin:index"))
        self.assertEqual(response.status_code, 200)

        # User is still authenticated
        updated_session = self.client.session
        self.assertEqual(updated_session.get("_auth_user_id"), str(self.staff_user.pk))

        # Activity timestamp was refreshed
        new_activity = get_last_activity(updated_session)
        self.assertGreater(new_activity, recent_activity)

    def test_ac3_ping_endpoint_reports_idle_seconds_and_logout_on_expiration(self):
        """AC3: GET /session_security/ping/?idleFor=N returns seconds since activity, or 'logout' when expired."""
        self.client.force_login(self.staff_user)

        now = datetime.now()
        session = self.client.session
        set_last_activity(session, now - timedelta(seconds=25))
        session.save()

        # 1. Active session ping
        ping_url = reverse("session_security_ping")
        response = self.client.get(f"{ping_url}?idleFor=25")
        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8").strip()
        # Inactivity response is integer seconds
        self.assertTrue(content.isdigit())

        # 2. Ping when session lacks _session_security (expired/logged out)
        anon_client = Client()
        anon_response = anon_client.get(f"{ping_url}?idleFor=650")
        self.assertEqual(anon_response.status_code, 200)
        self.assertEqual(anon_response.content.decode("utf-8").strip(), '"logout"')

    def test_ac4_jwt_api_request_is_unaffected_and_creates_no_session_security(self):
        """AC4: API request with valid JWT Authorization header and no session cookie is unaffected."""
        refresh = RefreshToken.for_user(self.regular_user)
        access_token = str(refresh.access_token)

        api_url = reverse("me")
        response = self.client.get(
            api_url,
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("email"), self.regular_user.email)

        # No session cookie or _session_security created
        session = self.client.session
        self.assertNotIn("_session_security", session)

    def test_ac5_admin_html_includes_bootstrap_only_for_staff(self):
        """AC5: Admin index HTML for logged-in staff contains SessionSecurity bootstrap; login page has neither."""
        # 1. Anonymous visitor on login page
        login_url = reverse("admin:login")
        login_response = self.client.get(login_url)
        self.assertEqual(login_response.status_code, 200)
        self.assertNotIn(
            "yourlabs.SessionSecurity", login_response.content.decode("utf-8")
        )

        # 2. Logged-in staff on admin index
        self.client.force_login(self.staff_user)
        admin_response = self.client.get(reverse("admin:index"))
        self.assertEqual(admin_response.status_code, 200)
        admin_html = admin_response.content.decode("utf-8")
        self.assertIn("yourlabs.SessionSecurity", admin_html)
        self.assertIn("admin/js/vendor/jquery/jquery.js", admin_html)

    def test_ac6_system_check_is_clean(self):
        """AC6: python manage.py check is clean, with no ImproperlyConfigured."""
        # call_command('check') will raise if check fails
        call_command("check")
