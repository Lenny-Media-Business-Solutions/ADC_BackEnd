from importlib import import_module

from django.apps import apps
from django.core.cache import cache
from django.db import migrations
from django.test import SimpleTestCase
from django.urls import Resolver404, resolve
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User


class StaffAuthenticationTests(APITestCase):
    def setUp(self):
        cache.clear()
        self.staff = User.objects.create_user(
            username='staff-user',
            email='staff@example.test',
            full_name='ADC Staff',
            password='StrongPass!123',
            role='staff',
        )
        self.admin = User.objects.create_user(
            username='portal-admin',
            email='admin@example.test',
            full_name='ADC Portal Admin',
            password='StrongPass!123',
            role='admin',
        )
        self.non_portal_user = User.objects.create_user(
            username='public-user',
            email='public@example.test',
            full_name='Non Portal User',
            password='StrongPass!123',
            role='visitor',
        )

    def test_active_staff_and_admin_receive_both_tokens(self):
        for user in (self.staff, self.admin):
            response = self.client.post(
                '/api/token/',
                {'username': user.username, 'password': 'StrongPass!123'},
                format='json',
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertTrue(response.data['access'])
            self.assertTrue(response.data['refresh'])

    def test_invalid_credentials_are_rejected(self):
        response = self.client.post(
            '/api/token/',
            {'username': self.staff.username, 'password': 'wrong-password'},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_inactive_and_non_portal_users_cannot_login(self):
        inactive_user = User.objects.create_user(
            username='inactive-staff',
            email='inactive@example.test',
            full_name='Inactive Staff',
            password='StrongPass!123',
            role='staff',
            is_active=False,
        )

        for user in (inactive_user, self.non_portal_user):
            response = self.client.post(
                '/api/token/',
                {'username': user.username, 'password': 'StrongPass!123'},
                format='json',
            )
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_staff_role_can_use_staff_api_but_non_portal_role_cannot(self):
        self.assertFalse(self.staff.is_staff)
        self.client.force_authenticate(user=self.non_portal_user)
        denied = self.client.get('/api/dashboard/summary/')
        self.assertEqual(denied.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user=self.staff)
        allowed = self.client.get('/api/dashboard/summary/')
        self.assertEqual(allowed.status_code, status.HTTP_200_OK)

    def test_user_management_is_admin_role_only(self):
        self.assertFalse(self.admin.is_staff)
        self.client.force_authenticate(user=self.staff)
        denied = self.client.get('/api/users/')
        self.assertEqual(denied.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user=self.admin)
        allowed = self.client.get('/api/users/')
        self.assertEqual(allowed.status_code, status.HTTP_200_OK)

    def test_profile_update_cannot_change_privilege_fields(self):
        self.client.force_authenticate(user=self.staff)
        response = self.client.patch(
            '/api/users/me/',
            {'role': 'admin', 'is_active': False, 'is_staff': True},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.staff.refresh_from_db()
        self.assertEqual(self.staff.role, 'staff')
        self.assertTrue(self.staff.is_active)
        self.assertFalse(self.staff.is_staff)

    def test_eligible_refresh_token_rotates(self):
        original_refresh = str(RefreshToken.for_user(self.staff))
        response = self.client.post(
            '/api/token/refresh/', {'refresh': original_refresh}, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['access'])
        self.assertTrue(response.data['refresh'])
        self.assertNotEqual(response.data['refresh'], original_refresh)

    def test_refresh_rejects_ineligible_account_before_rotation(self):
        original_refresh = str(RefreshToken.for_user(self.staff))
        self.staff.role = 'visitor'
        self.staff.save(update_fields=['role'])

        denied = self.client.post(
            '/api/token/refresh/', {'refresh': original_refresh}, format='json'
        )
        self.assertEqual(denied.status_code, status.HTTP_401_UNAUTHORIZED)

        self.staff.role = 'staff'
        self.staff.save(update_fields=['role'])
        eligible_again = self.client.post(
            '/api/token/refresh/', {'refresh': original_refresh}, format='json'
        )
        self.assertEqual(eligible_again.status_code, status.HTTP_200_OK)

    def test_refresh_rejects_inactive_or_missing_account(self):
        inactive_refresh = str(RefreshToken.for_user(self.staff))
        self.staff.is_active = False
        self.staff.save(update_fields=['is_active'])
        inactive = self.client.post(
            '/api/token/refresh/', {'refresh': inactive_refresh}, format='json'
        )
        self.assertEqual(inactive.status_code, status.HTTP_401_UNAUTHORIZED)

        self.staff.is_active = True
        self.staff.save(update_fields=['is_active'])
        deleted_user = User.objects.create_user(
            username='deleted-user',
            email='deleted@example.test',
            full_name='Deleted User',
            password='StrongPass!123',
            role='staff',
        )
        missing_user_refresh = str(RefreshToken.for_user(deleted_user))
        deleted_user.delete()
        missing_user = self.client.post(
            '/api/token/refresh/',
            {'refresh': missing_user_refresh},
            format='json',
        )
        self.assertEqual(missing_user.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_is_throttled_after_five_attempts_per_minute(self):
        responses = [
            self.client.post(
                '/api/token/',
                {'username': 'unknown-user', 'password': 'wrong-password'},
                format='json',
            )
            for _ in range(6)
        ]
        self.assertEqual(
            [response.status_code for response in responses[:5]],
            [status.HTTP_401_UNAUTHORIZED] * 5,
        )
        self.assertEqual(responses[5].status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class OTPRemovalTests(SimpleTestCase):
    def test_otp_verification_route_is_removed(self):
        with self.assertRaises(Resolver404):
            resolve('/api/token/verify-2fa/')

    def test_otp_model_is_not_registered(self):
        model_names = {model.__name__ for model in apps.get_app_config('users').get_models()}
        self.assertNotIn('OTPVerification', model_names)

    def test_followup_migration_deletes_historical_otp_model(self):
        migration = import_module(
            'users.migrations.0004_delete_otpverification'
        ).Migration
        self.assertIn(('users', '0003_otpverification'), migration.dependencies)
        self.assertTrue(
            any(
                isinstance(operation, migrations.DeleteModel)
                and operation.name == 'OTPVerification'
                for operation in migration.operations
            )
        )
