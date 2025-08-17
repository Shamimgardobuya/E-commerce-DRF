from unittest.mock import patch
from django.urls import reverse
from rest_framework.test import APITestCase

class CategoryApiViewTests(APITestCase):
    @patch("categories.views.Category.objects.get_or_create")
    def test_post_category(self, mock_get_or_create):
        # mock what get_or_create returns (tuple: (object, created_bool))
        mock_get_or_create.return_value = (
            type("Category", (), {"id": 1, "category_name": "Electronics"})(),
            True,
        )

        url = reverse("category")  # adjust to your route
        payload = {
            "category_name": "Phones",
            "parent_category": "Electronics"
        }
        response = self.client.post(url, payload, format="json")

        # assertions
        self.assertEqual(response.status_code, 201)
        self.assertIn("Category created successfully", str(response.data))

        # make sure get_or_create was called twice
        self.assertEqual(mock_get_or_create.call_count, 2)
