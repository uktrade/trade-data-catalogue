from unittest.mock import patch, MagicMock
from django.test import TestCase, RequestFactory
from django.urls import reverse

from dataset_catalogue.views import DatasetDetailsView


class TestDatasetDetailView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.view = DatasetDetailsView()

    def test_view_is_instance_of_class(self):
        self.assertIsInstance(self.view, DatasetDetailsView)

    @patch("dataset_catalogue.views.DatasetDetails")
    def test_get_context_data_with_kwargs(self, MockDatasetDetails):
        mock_kwargs = {"dataset_id": "mock-dataset", "version": "v1.0.0"}

        request = self.factory.get("/mock-dataset/v1.0.0")
        request.kwargs = mock_kwargs

        self.view.request = request

        mock_dataset_details_instance = MagicMock()

        mock_dataset_details_instance.id = "mock-dataset"
        mock_dataset_details_instance.version = "v1.0.0"

        MockDatasetDetails.return_value = mock_dataset_details_instance

        response = self.client.get(
            reverse(
                "dataset_details_view",
                kwargs=mock_kwargs,
            )
        )

        self.assertEqual(
            response.context["dataset"],
            mock_dataset_details_instance,
        )
