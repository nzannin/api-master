from django.test import TestCase
from api.models import Order, User
from django.urls import reverse
from rest_framework import status

# Create your tests here.
class UserOrderTestCase(TestCase):
    """
    Test case for user order functionality.
    """
    
    def setUp(self):
        user1 = User.objects.create_user(
            username='user1',
            password='user1',
        )
        user2 = User.objects.create_user(
            username='user2',
            password='user2',
        )
        Order.objects.create(
            user=user1)
        Order.objects.create(
            user=user1)
        Order.objects.create(
            user=user2)
        Order.objects.create(
            user=user2)
        
    def test_user_order_endpoint_retrieves_only_authenticated_user_orders(self):
        """
        Test that the user order endpoint retrieves only orders for the authenticated user.
        """
        user = User.objects.get(username='user2')
        self.client.force_login(user)
        response = self.client.get(reverse('user-orders'))
        assert response.status_code == status.HTTP_200_OK
        orders = response.json()
        self.assertTrue(all(order['user'] == user.id for order in orders))

    def test_user_order_list_unauthenticated(self):
        """
        Test that the user order list endpoint returns a 403 status code for unauthenticated users.
        """
        response = self.client.get(reverse('user-orders'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

