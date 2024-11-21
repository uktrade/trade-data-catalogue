from unittest.mock import patch, MagicMock
from django.test import TestCase, RequestFactory
from django.urls import reverse

from dataset_catalogue.views import DatasetDetailsView


class TestDatasetDetailView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.view = DatasetDetailsView()
        self.mock_valid_dataset_details_instance = MagicMock()

        self.mock_valid_dataset_details_instance.id = "mock-dataset"
        self.mock_valid_dataset_details_instance.version = "v1.0.0"

        self.mock_table_object_instance = MagicMock()
        self.mock_report_object_instance = MagicMock()

        self.mock_table_object_instance.id = "mock-table"
        self.mock_report_object_instance.id = "mock-report"

    def test_view_is_instance_of_class(self):
        self.assertIsInstance(self.view, DatasetDetailsView)

    @patch("dataset_catalogue.views.DatasetDetails")
    def test_get_context_data_with_kwargs(self, MockDatasetDetails):
        mock_kwargs = {"dataset_id": "mock-dataset", "version": "v1.0.0"}

        request = self.factory.get("/mock-dataset/v1.0.0")
        request.kwargs = mock_kwargs

        self.view.request = request

        MockDatasetDetails.return_value = self.mock_valid_dataset_details_instance

        response = self.client.get(
            reverse(
                "dataset_details_view",
                kwargs=mock_kwargs,
            )
        )

        self.assertEqual(
            response.context["dataset"],
            self.mock_valid_dataset_details_instance,
        )

    @patch("dataset_catalogue.views.DatasetDetails")
    def test_get_context_data_with_kwargs_has_tables(self, MockDatasetDetails):
        mock_kwargs = {"dataset_id": "mock-dataset", "version": "v1.0.0"}

        request = self.factory.get("/mock-dataset/v1.0.0")
        request.kwargs = mock_kwargs

        self.view.request = request

        self.mock_valid_dataset_details_instance.tables = [
            self.mock_table_object_instance
        ]

        MockDatasetDetails.return_value = self.mock_valid_dataset_details_instance

        response = self.client.get(
            reverse(
                "dataset_details_view",
                kwargs=mock_kwargs,
            )
        )

        self.assertEqual(
            list(response.context["tables_page"]),
            self.mock_valid_dataset_details_instance.tables,
        )

    @patch("dataset_catalogue.views.DatasetDetails")
    def test_get_context_data_with_kwargs_has_reports(self, MockDatasetDetails):
        mock_kwargs = {"dataset_id": "mock-dataset", "version": "v1.0.0"}

        request = self.factory.get("/mock-dataset/v1.0.0")
        request.kwargs = mock_kwargs

        self.view.request = request

        self.mock_valid_dataset_details_instance.reports = [
            self.mock_report_object_instance
        ]

        MockDatasetDetails.return_value = self.mock_valid_dataset_details_instance

        response = self.client.get(
            reverse(
                "dataset_details_view",
                kwargs=mock_kwargs,
            )
        )

        self.assertEqual(
            list(response.context["reports_page"]),
            self.mock_valid_dataset_details_instance.reports,
        )

    @patch("dataset_catalogue.views.DatasetDetails")
    def test_get_context_data_with_kwargs_has_tables_and_reports(
        self, MockDatasetDetails
    ):
        mock_kwargs = {"dataset_id": "mock-dataset", "version": "v1.0.0"}

        request = self.factory.get("/mock-dataset/v1.0.0")
        request.kwargs = mock_kwargs

        self.view.request = request

        self.mock_valid_dataset_details_instance.tables = [
            self.mock_table_object_instance
        ]
        self.mock_valid_dataset_details_instance.reports = [
            self.mock_report_object_instance
        ]

        MockDatasetDetails.return_value = self.mock_valid_dataset_details_instance

        response = self.client.get(
            reverse(
                "dataset_details_view",
                kwargs=mock_kwargs,
            )
        )

        self.assertEqual(
            list(response.context["tables_page"]),
            self.mock_valid_dataset_details_instance.tables,
        )
        self.assertEqual(
            list(response.context["reports_page"]),
            self.mock_valid_dataset_details_instance.reports,
        )
