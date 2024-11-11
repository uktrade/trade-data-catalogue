from unittest.mock import patch
from django.test import TestCase

from dataset_catalogue.models import Dataset


class TestDatasetModel(TestCase):
    def test_get_formatted_dataset_title(self):
        dataset = Dataset(id="mock-dataset")
        result = dataset.get_formatted_dataset_title(dataset.id)
        self.assertEqual(result, "Mock Dataset")
    
    @patch("dataset_catalogue.models.fetch_json_data_from_api")
    def test_get_dataset_versions(self, mock_fetch_dataset_api_data,):
        mock_fetch_dataset_api_data.return_value = {
            "versions": [
            {
                "id": "v1.0.0"
            }
            ]
        }
        dataset = Dataset(id="mock-dataset")
        result = dataset.get_dataset_versions(dataset.url)
        self.assertEqual(result, ["v1.0.0"])
    
    