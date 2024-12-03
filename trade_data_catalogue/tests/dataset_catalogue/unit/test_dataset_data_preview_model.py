from unittest.mock import patch, MagicMock
from django.test import TestCase

from dataset_catalogue.models import DatasetDataPreview


class TestDatasetDataPreviewModel(TestCase):
    @patch("dataset_catalogue.models.DatasetTable")
    def test_object_initialises_with_table_type(self, MockDatasetTable):
        mock_table_instance = MagicMock()
        mock_table_instance.id = "mock-table"

        MockDatasetTable.return_value = mock_table_instance

        mock_valid_dataset_data_preview_instance = DatasetDataPreview(
            "mock-dataset", "v1.0.0", "table", "mock-table"
        )
        mock_table_instance.dataset = mock_valid_dataset_data_preview_instance

        self.assertEqual(
            mock_valid_dataset_data_preview_instance.data_object, mock_table_instance
        )

    @patch("dataset_catalogue.models.DatasetReport")
    def test_object_initialises_with_report_type(self, MockDatasetReport):
        mock_report_instance = MagicMock()
        mock_report_instance.id = "mock-report"

        MockDatasetReport.return_value = mock_report_instance

        mock_valid_dataset_data_preview_instance = DatasetDataPreview(
            "mock-dataset", "v1.0.0", "report", "mock-report"
        )
        mock_report_instance.dataset = mock_valid_dataset_data_preview_instance

        self.assertEqual(
            mock_valid_dataset_data_preview_instance.data_object, mock_report_instance
        )

    @patch("dataset_catalogue.models.fetch_data_from_api")
    def test_dataset_data_preview_metadata(self, mock_fetch_data_from_api):
        mock_fetch_data_from_api = {
            "tables": [
                {
                    "url": "mock-table",
                    "tableSchema": {
                        "columns": [{"name": "col_1", "description": "col_description"}]
                    },
                }
            ]
        }
