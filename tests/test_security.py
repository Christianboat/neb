import os
import re
import sys
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import (
    SiteSettings, ContactInfo, InquiryType, User, Inquiry,
)
from config import TestingConfig


class CSRFTestConfig(TestingConfig):
    """Like TestingConfig but with CSRF enabled so we can verify protection."""
    WTF_CSRF_ENABLED = True
    SERVER_NAME = 'localhost'


def _extract_token(html):
    match = re.search(r'name="csrf_token"[^>]*value="([^"]+)"', html)
    return match.group(1) if match else None


class SecurityTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(CSRFTestConfig)
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()
        db.session.add(SiteSettings(site_name='Nebula Test'))
        db.session.add(ContactInfo(email='test@example.com', phone='+1'))
        db.session.add(InquiryType(name='General', value='general'))
        admin = User(username='admin')
        admin.set_password('StrongPass123!')
        db.session.add(admin)
        db.session.commit()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    # --- Security headers ---
    def test_security_headers_present(self):
        r = self.client.get('/')
        self.assertIn('Content-Security-Policy', r.headers)
        self.assertEqual(r.headers.get('X-Frame-Options'), 'SAMEORIGIN')
        self.assertEqual(
            r.headers.get('X-Content-Type-Options'), 'nosniff')

    # --- Error pages ---
    def test_custom_404_page(self):
        r = self.client.get('/no-such-page')
        self.assertEqual(r.status_code, 404)
        self.assertIn(b'404', r.data)

    # --- SEO endpoints ---
    def test_robots_txt(self):
        r = self.client.get('/robots.txt')
        self.assertEqual(r.status_code, 200)
        self.assertIn(b'Disallow: /admin/', r.data)

    def test_sitemap_xml(self):
        r = self.client.get('/sitemap.xml')
        self.assertEqual(r.status_code, 200)
        self.assertIn(b'<urlset', r.data)

    # --- CSRF on the public contact form ---
    def test_contact_post_without_csrf_is_rejected(self):
        r = self.client.post('/contact', data={
            'name': 'Bot', 'email': 'b@b.com', 'message': 'hi'})
        self.assertEqual(r.status_code, 400)

    def test_contact_post_with_csrf_succeeds(self):
        page = self.client.get('/contact').get_data(as_text=True)
        token = _extract_token(page)
        self.assertIsNotNone(token)
        r = self.client.post('/contact', data={
            'csrf_token': token, 'name': 'Jane', 'email': 'j@x.com',
            'message': 'Hello there', 'form_timestamp': '1'})
        self.assertEqual(r.status_code, 302)
        self.assertEqual(Inquiry.query.count(), 1)

    # --- Admin auth ---
    def test_admin_requires_login(self):
        r = self.client.get('/admin/dashboard')
        self.assertIn(r.status_code, (301, 302))

    def test_admin_login_and_protected_action(self):
        login_page = self.client.get('/admin/login').get_data(as_text=True)
        token = _extract_token(login_page)
        r = self.client.post('/admin/login', data={
            'csrf_token': token, 'username': 'admin',
            'password': 'StrongPass123!'})
        self.assertEqual(r.status_code, 302)
        r = self.client.get('/admin/dashboard')
        self.assertEqual(r.status_code, 200)

    def test_admin_login_wrong_password(self):
        login_page = self.client.get('/admin/login').get_data(as_text=True)
        token = _extract_token(login_page)
        r = self.client.post('/admin/login', data={
            'csrf_token': token, 'username': 'admin',
            'password': 'wrong'}, follow_redirects=True)
        self.assertIn(b'Invalid username or password', r.data)


if __name__ == '__main__':
    unittest.main(verbosity=2)
