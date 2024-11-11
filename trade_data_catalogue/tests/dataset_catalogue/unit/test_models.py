from unittest.mock import patch
from django.test import TestCase

from dataset_catalogue.models import Dataset


class TestDatasetModel(TestCase):
    def test_get_formatted_dataset_title(self):
        dataset = Dataset(id="mock-dataset")
        result = dataset.get_formatted_dataset_title(dataset.id)
        self.assertEqual(result, "Mock Dataset")