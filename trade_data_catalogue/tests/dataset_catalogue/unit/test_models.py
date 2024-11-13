from unittest.mock import patch
from django.test import TestCase

from dataset_catalogue.models import Dataset


class TestDatasetModel(TestCase):
    def test_get_formatted_dataset_title(self):
        dataset = Dataset(id="mock-dataset")
        result = dataset.get_formatted_dataset_title(dataset.id)
        self.assertEqual(result, "Mock Dataset")

    @patch("dataset_catalogue.models.fetch_data_from_api")
    def test_get_dataset_versions(
        self,
        mock_fetch_dataset_api_data,
    ):
        mock_fetch_dataset_api_data.return_value = {"versions": [{"id": "v1.0.0"}]}
        dataset = Dataset(id="mock-dataset")
        result = dataset.get_dataset_versions(dataset.url)
        self.assertEqual(result, ["v1.0.0"])

    def test_get_number_of_dataset_versions(self):
        dataset = Dataset(id="mock-dataset")
        dataset.versions = ["v1.0.1", "v1.0.0"]
        result = dataset.get_number_of_dataset_versions(dataset.versions)
        self.assertEqual(result, 2)

    def test_get_version_count_message_single(self):
        dataset = Dataset(id="mock-dataset")
        dataset.versions_count = 1
        result = dataset.get_version_count_message(dataset.versions_count)
        self.assertEqual(result, "1 version")

    def test_get_version_count_message_plural(self):
        dataset = Dataset(id="mock-dataset")
        dataset.versions_count = 2
        result = dataset.get_version_count_message(dataset.versions_count)
        self.assertEqual(result, "2 versions")

    def test_get_latest_version(self):
        dataset = Dataset(id="mock-dataset")
        dataset.versions = ["v1.0.1", "v1.0.0"]
        result = dataset.get_latest_version(dataset.versions)
        self.assertEqual(result, "v1.0.1")
