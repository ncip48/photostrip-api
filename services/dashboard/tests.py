from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from services.account.models import User
from services.transaction.models import TopupTransaction
from services.photostrip.models import Photostrip
from services.product.models import Product
from services.file.models import File
from decimal import Decimal

class DashboardStatsTests(APITestCase):
    def setUp(self):
        # Create user
        self.user = User.objects.create_user(
            email="test@example.com",
            username="testuser",
            password="password123",
            first_name="Test",
            last_name="User"
        )
        self.client.force_authenticate(user=self.user)

        # Create product
        self.product = Product.objects.create(
            token=Decimal("100.00"),
            price=Decimal("10.00")
        )

        # Create transaction (success)
        TopupTransaction.objects.create(
            user=self.user,
            reference="REF001",
            product=self.product,
            token=Decimal("100.00"),
            total=Decimal("10.00"),
            status=TopupTransaction.Status.SUCCESS,
            provider="test"
        )
        # Create transaction (pending - shouldn't count)
        TopupTransaction.objects.create(
            user=self.user,
            reference="REF002",
            product=self.product,
            token=Decimal("100.00"),
            total=Decimal("10.00"),
            status=TopupTransaction.Status.PENDING,
            provider="test"
        )

        # Create file
        self.file = File.objects.create(
            encrypted_file="test.jpg",
            encryption_iv="iv",
            encrypted_key="key"
        )

        # Create photostrip
        Photostrip.objects.create(
            user=self.user,
            file=self.file
        )

    def test_dashboard_stats_users(self):
        url = reverse("dashboard:stats-users")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_dashboard_stats_topups(self):
        url = reverse("dashboard:stats-topups")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_dashboard_stats_photostrips(self):
        url = reverse("dashboard:stats-photostrips")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
