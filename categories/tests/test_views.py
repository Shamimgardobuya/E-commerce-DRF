from django.urls import reverse
from rest_framework.test import APITestCase
from unittest.mock import patch
from rest_framework import status
from registration.models import Customer
from django.contrib.auth import get_user_model
from categories.models import Category

@patch('registration.utils.Auth0JWTAuthentication.decode_token')
@patch('registration.utils.Auth0JWTAuthentication.authenticate')
class CategoryCreationTests(APITestCase):

    def setUp(self):
        Customer.objects.get_or_create(open_id='test-user-id')
        parent_category , create_parent_category = Category.objects.get_or_create(category_name='Bags')
        child_category = Category.objects.get_or_create(category_name="leather2 bag",parent=parent_category)


    def test_create_category_with_permission(self, mock_authenticate, mock_decode_token):

        mock_authenticate.return_value = (Customer.objects.get(open_id='test-user-id'), 'fake-token')
        mock_decode_token.return_value = {
            'sub': 'test-user-id',
            'scope': 'create:categories read:categories'
        }
        
        url = reverse('category_list')
        headers = {'HTTP_AUTHORIZATION': 'Bearer fake-token'}
        data = {'category_name':  'Leather Bags', 'parent_category': 'Bags'}
        response = self.client.post(url, data, **headers, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_create_category_without_permission(self, mock_authenticate, mock_decode_token):
        mock_authenticate.return_value = (Customer.objects.get(open_id='test-user-id'), 'fake-token')
        
        mock_decode_token.return_value = {
            'sub': 'test-user-id',
            'scope': 'read:categories'
        }
        
        url = reverse('category_list')
        headers = {'HTTP_AUTHORIZATION': 'Bearer fake-token'}
        data = {'category_name': 'Leather Bags', 'parent_category': 'bags'}
        response = self.client.post(url, data, **headers, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_update_category_with_permission(self, mock_authenticate, mock_decode_token):
        mock_authenticate.return_value = (Customer.objects.get(open_id='test-user-id'), 'fake-token')
        mock_decode_token.return_value = {
            'sub': 'test-user-id',
            'scope': 'update:categories read:categories'
        }
        existing_category = Category.objects.get(category_name='leather2 bag')
        url = reverse('category_detail', args=[existing_category.id])
        headers = { 'HTTP_AUTHORIZATION' : 'Bearer fake-token'}
        data = {'category_name': 'Cotton Bags', 'parent_category': 'Bags'}
        response = self.client.put(url, data,**headers)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        
