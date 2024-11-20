from unittest.mock import patch, MagicMock
from django.test import TestCase
from django.urls import reverse

from dataset_catalogue.views import DatasetCatalogueView
from dataset_catalogue.models import Dataset


class TestDatasetCatalogueView(TestCase):
    def setUp(self):
        self.view = DatasetCatalogueView()

    def test_view_is_instance_of_class(self):
        self.assertIsInstance(self.view, DatasetCatalogueView)

    def test_get_dataset_ids_extracts_dataset_id(self):
        mock_api_json_response = {"datasets": [{"id": "mock_dataset_id"}]}
        result = self.view.get_dataset_ids(mock_api_json_response)
        expected_value = ["mock_dataset_id"]

        self.assertEqual(result, expected_value)

    @patch("dataset_catalogue.models.fetch_data_from_api")
    @patch("dataset_catalogue.views.Dataset")
    def test_get_dataset_objects(self, MockDataset, mock_fetch_dataset_api_data):
        mock_fetch_dataset_api_data.return_value = {
            "versions": [{"id": "v1.1"}, {"id": "v1.0"}]
        }
        mock_dataset_ids = ["mock-dataset"]
        mock_dataset_instance = MagicMock(spec=Dataset)

        mock_dataset_instance.get_formatted_dataset_title.return_value = "Mock Dataset"
        mock_dataset_instance.get_all_dataset_versions.return_value = ["v1.1", "v1.0"]
        mock_dataset_instance.get_number_of_dataset_versions.return_value = 2
        mock_dataset_instance.get_version_count_message.return_value = "2 versions"
        mock_dataset_instance.get_latest_version.return_value = "v1.1"
        mock_dataset_instance.versions = ["v1.1", "v1.0"]

        MockDataset.return_value = mock_dataset_instance

        result = self.view.get_dataset_objects(mock_dataset_ids)
        expected_value = {"mock-dataset": mock_dataset_instance}

        self.assertEqual(result, expected_value)

    @patch.object(DatasetCatalogueView, "get_dataset_objects")
    def test_view_renders_correct_template_and_context(
        self,
        mock_get_dataset_objects,
    ):
        mock_dataset_instance = MagicMock()
        mock_dataset_instance.id = "mock-dataset"
        mock_dataset_instance.title = "Mock Dataset"
        mock_dataset_instance.versions = ["v1.1", "v1.0"]
        mock_dataset_instance.versions_count = 2
        mock_dataset_instance.version_count_message = "2 versions"
        mock_dataset_instance.latest_version = "v1.1"

        mock_get_dataset_objects.return_value = {"mock-dataset": mock_dataset_instance}

        response = self.client.get(reverse("dataset_catalogue_view"))

        self.assertEqual(
            response.context["datasets"], {"mock-dataset": mock_dataset_instance}
        )
        self.assertEqual(response.context["dataset_count"], 1)

        expected_template_name = "dataset_catalogue/catalogue.html"

        self.assertTemplateUsed(response, expected_template_name)
