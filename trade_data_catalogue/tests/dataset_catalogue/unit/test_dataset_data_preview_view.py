from unittest.mock import patch, MagicMock
from django.test import TestCase, RequestFactory
from django.urls import reverse

from dataset_catalogue.views import DatasetDataPreviewView


class TestDatasetDataPreviewView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.view = DatasetDataPreviewView()
        self.mock_valid_dataset_data_preview_instance = MagicMock()

        self.mock_valid_dataset_data_preview_instance.id = "mock-dataset"
        self.mock_valid_dataset_data_preview_instance.version = "v1.0.0"

        self.mock_valid_data_object_instance = MagicMock()

        self.mock_valid_data_object_instance.id = "mock-table"
        self.mock_valid_data_object_instance.csv_headers = [
            "header_1",
            "header_2",
            "header_3",
        ]
        self.mock_valid_data_object_instance.csv_rows = [
            ["r1_cell_1", "r1_cell_2", "r1_cell_3"],
            ["r2_cell_1", "r2_cell_2", "r2_cell_3"],
            ["r3_cell_1", "r3_cell_2", "r3_cell_3"],
        ]
        self.mock_valid_data_object_instance.csv_row_count = 3

        self.mock_kwargs = {
            "dataset_id": "mock-dataset",
            "version": "v1.0.0",
            "data_type": "table",
            "data_id": "mock-table",
        }

    def test_view_is_instance_of_class(self):
        self.assertIsInstance(self.view, DatasetDataPreviewView)

    @patch("dataset_catalogue.views.DatasetDataPreview")
    def test_get_context_data_with_kwargs(self, MockDatasetDataPreview):
        request = self.factory.get("/dataset-id-mock-dataset/v1.0.0/table/mock-table")
        request.kwargs = self.mock_kwargs

        self.view.request = request

        MockDatasetDataPreview.return_value = (
            self.mock_valid_dataset_data_preview_instance
        )

        response = self.client.get(
            reverse(
                "dataset_data_preview_view",
                kwargs=self.mock_kwargs,
            )
        )

        self.assertEqual(
            response.context["dataset"],
            self.mock_valid_dataset_data_preview_instance,
        )

    @patch("dataset_catalogue.views.DatasetDataPreview")
    def test_get_context_data_with_kwargs_has_data_object_and_csv_data(
        self, MockDatasetDataPreview
    ):
        request = self.factory.get("/dataset-id-mock-dataset/v1.0.0/table/mock-table")
        request.kwargs = self.mock_kwargs

        self.view.request = request

        self.mock_valid_dataset_data_preview_instance.data_object = (
            self.mock_valid_data_object_instance
        )

        MockDatasetDataPreview.return_value = (
            self.mock_valid_dataset_data_preview_instance
        )

        response = self.client.get(
            reverse(
                "dataset_data_preview_view",
                kwargs=self.mock_kwargs,
            )
        )

        self.assertEqual(
            response.context["dataset"].data_object,
            self.mock_valid_data_object_instance,
        )
        self.assertEqual(
            response.context["data_headers"],
            self.mock_valid_data_object_instance.csv_headers,
        )
        self.assertEqual(
            response.context["row_count"],
            self.mock_valid_data_object_instance.csv_row_count,
        )
        self.assertEqual(
            list(response.context["rows_page"]),
            self.mock_valid_data_object_instance.csv_rows,
        )

    def test_download_csv(self):
        self.mock_valid_dataset_data_preview_instance.data_object = (
            self.mock_valid_data_object_instance
        )

        response = self.view.download_csv(self.mock_valid_dataset_data_preview_instance)

        self.assertEqual(
            response["Content-Disposition"],
            'attachment; filename="mock-dataset-v1.0.0-mock-table.csv"',
        )
        self.assertEqual(response["Content-Type"], "text/csv")

        content = response.content.decode("utf-8")
        rows = content.split("\r\n")

        self.assertEqual(rows[0], "header_1,header_2,header_3")
        self.assertEqual(rows[1], "r1_cell_1,r1_cell_2,r1_cell_3")
        self.assertEqual(rows[2], "r2_cell_1,r2_cell_2,r2_cell_3")
        self.assertEqual(rows[3], "r3_cell_1,r3_cell_2,r3_cell_3")
