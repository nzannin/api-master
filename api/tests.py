from api.models import Product, User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status


# Test cases
class ProductAPITests(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username='admin',
            password='adminpassword',
        )
        self.normal_user = User.objects.create_user(
            username='user',
            password='userpassword',
        )
        self.product = Product.objects.create(
            name='Test Product',
            description='A product for testing',
            price=10.00,
            stock=100
        )
        self.url = reverse('product-detail', kwargs={'pk': self.product.pk})
        
    def test_get_product(self):
        """
        Test retrieving a product by ID.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.product.name) 
        self.assertEqual(response.data['description'], self.product.description)

    def test_unauthorized_update_product(self):
        """
        Test updating a product without authentication.
        """
        data = {'name': 'Updated Product'}
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_unauthorized_delete_product(self):
        """
        Test deleting a product without authentication.
        """
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_only_admin_can_delete_product(self):
        """
        Test that only admin users can delete a product.
        """
        self.client.login(username='user', password='userpassword')
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Product.objects.filter(pk=self.product.pk).exists())

        self.client.logout()
        
        self.client.login(username='admin', password='adminpassword')
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(pk=self.product.pk).exists())  