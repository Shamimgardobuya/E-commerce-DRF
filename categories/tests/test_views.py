from django.urls import reverse
from rest_framework.test import APITestCase
from unittest.mock import patch
from rest_framework import status
from registration.models import Customer
from categories.models import Category
from products.models import Product
from decimal import Decimal
@patch('registration.utils.Auth0JWTAuthentication.decode_token')
@patch('registration.utils.Auth0JWTAuthentication.authenticate')
class CategoryCreationTests(APITestCase):

    def setUp(self):
        self.customer, create_customer = Customer.objects.get_or_create(open_id='test-user-id')
        self.parent_category , create_parent_category = Category.objects.get_or_create(category_name='Bags')
        self.child_category_a, new_child_category_a = Category.objects.get_or_create(category_name="leather2 bag",parent=self.parent_category)
        self.product, create_product = Product.objects.get_or_create(name="grey bag", price=200.00, category=self.child_category_a,weight=34,quantity=45, units="grams")
        self.child_category_b, new_child_category_b = Category.objects.get_or_create(category_name="silk bag",parent=self.parent_category)
        self.product, create_product = Product.objects.get_or_create(name="grey bag", price=300.00, category=self.child_category_b,weight=34,quantity=45, units="grams")

    def mock_auth(self, mock_authenticate, mock_decode_token, permissions):
        mock_authenticate.return_value = (self.customer, 'fake-token')
        mock_decode_token.return_value = {
            'sub': self.customer.open_id,
            'permissions': permissions
        }
        return {'HTTP_AUTHORIZATION': 'Bearer fake-token'}

    def test_create_category_with_permission(self, mock_authenticate, mock_decode_token):
        headers = self.mock_auth(mock_authenticate, mock_decode_token,['create:categories'] )
        url = reverse('category_list')
        data = {'category_name':  'Leather Bags', 'parent_category': 'Bags'}
        response = self.client.post(url, data, **headers, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_create_category_without_permission(self, mock_authenticate, mock_decode_token):
        headers = self.mock_auth(mock_authenticate, mock_decode_token,['read:categories'] )
        
        url = reverse('category_list')
        data = {'category_name': 'Leather Bags', 'parent_category': 'bags'}
        response = self.client.post(url, data, **headers, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_get_all_categories(self, mock_authenticate, mock_decode_token):
        headers = self.mock_auth(mock_authenticate, mock_decode_token,['read:categories'] )
        url = reverse('category_list')
        response = self.client.get(url, **headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_get_average_product(self, mock_authenticate, mock_decode_token):
        headers = self.mock_auth(mock_authenticate, mock_decode_token, ['read:categories'])
        url = reverse('category_detail', args=[self.parent_category.id])
        response = self.client.get(url,{"average_price": "true"}, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data'],(Decimal('250.0000000000000000'),))
        
    def test_update_category_with_permission(self, mock_authenticate, mock_decode_token):
        headers = self.mock_auth(mock_authenticate, mock_decode_token, ['update:categories', 'read:categories'])
        existing_category = Category.objects.get(category_name='leather2 bag')
        url = reverse('category_detail', args=[existing_category.id])
        data = {'category_name': 'Cotton Bags', 'parent_category': 'Bags'}
        response = self.client.put(url, data,**headers)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['category_name'],'Cotton Bags' )
        
    def test_retrieve_category_with_permission(self, mock_authenticate, mock_decode_token):
        headers = self.mock_auth(mock_authenticate, mock_decode_token, ['read:categories'])
        existing_category = Category.objects.get(category_name='leather2 bag')
        url = reverse('category_detail', args=[existing_category.id])
        response = self.client.get(url, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['category_name'],'leather2 bag' )

        
    def test_retrieve_non_existent_category(self, mock_authenticate, mock_decode_token):
        headers = self.mock_auth(mock_authenticate, mock_decode_token, ['read:categories'])
        url = reverse('category_detail', args=[8])
        response = self.client.get(url, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_deleting_existing_category(self, mock_authenticate, mock_decode_token):
        headers = self.mock_auth(mock_authenticate, mock_decode_token, ['delete:categories'])
        category, new_category = Category.objects.get_or_create(category_name='test')
        url = reverse('category_detail', args=[category.id])
        response = self.client.delete(url, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_deleting_existing_category_linked(self, mock_authenticate, mock_decode_token):
        headers = self.mock_auth(mock_authenticate, mock_decode_token, ['delete:categories'])
        url = reverse('category_detail', args=[self.parent_category.id])
        response = self.client.delete(url, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def tearDown(self):
        return super().tearDown()
