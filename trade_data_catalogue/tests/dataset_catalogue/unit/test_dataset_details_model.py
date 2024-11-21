from unittest.mock import patch
from django.test import TestCase

from dataset_catalogue.models import DatasetDetails

class TestDatasetDetailsModel(TestCase):
    def setUp(self):
        self.mock_valid_dataset_details_instance = DatasetDetails(id="mock-dataset", version="v1.0.0")
        self.mock_valid_dataset_details_instance.versions = ["v1.0.0"]

    @patch("dataset_catalogue.models.fetch_data_from_api")
    def test_get_dataset_metadata(self, mock_fetch_dataset_details_api_data):
        mock_fetch_dataset_details_api_data.return_value = {"mock_key": "mock_value"}

        result = self.mock_valid_dataset_details_instance.get_dataset_metadata(self.mock_valid_dataset_details_instance.url)
        self.assertEqual(result, {"mock_key": "mock_value"})
    
    @patch("dataset_catalogue.models.fetch_data_from_api")
    def test_dataset_has_no_metadata(self, mock_fetch_dataset_details_api_data):
        mock_fetch_dataset_details_api_data.return_value = None
        result = self.mock_valid_dataset_details_instance.get_dataset_metadata(self.mock_valid_dataset_details_instance.url)
        self.assertEqual(result, None)
    