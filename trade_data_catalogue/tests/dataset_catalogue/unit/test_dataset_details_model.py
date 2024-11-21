from unittest.mock import patch, MagicMock
from django.test import TestCase

from dataset_catalogue.models import DatasetDetails

class TestDatasetDetailsModel(TestCase):
    def setUp(self):
        self.mock_valid_dataset_details_instance = DatasetDetails(id="mock-dataset", version="v1.0.0")
        self.mock_valid_dataset_details_instance.versions = ["v1.0.0"]
        self.mock_valid_dataset_details_instance.table_ids = ["mock-table-id"]
        self.mock_valid_dataset_details_instance.report_ids = ["mock-report-id"]

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

    @patch("dataset_catalogue.models.fetch_data_from_api")
    def test_get_dataset_table_ids(self, mock_fetch_dataset_details_api_data):
        mock_fetch_dataset_details_api_data.return_value = {"tables": [{"id": "mock-table-id"}]}
        result = self.mock_valid_dataset_details_instance.get_dataset_table_ids(self.mock_valid_dataset_details_instance.url)
        self.assertEqual(result, ["mock-table-id"])
    
    @patch("dataset_catalogue.models.DatasetTable")
    def test_get_dataset_table_objects(self, MockDatasetTable):
        mock_table_instance = MagicMock()
        mock_table_instance.id = "mock-table-id"
        mock_table_instance.dataset = self.mock_valid_dataset_details_instance

        MockDatasetTable.return_value = mock_table_instance

        result = self.mock_valid_dataset_details_instance.get_dataset_table_objects(self.mock_valid_dataset_details_instance.table_ids)
        expected_value = [mock_table_instance]

        self.assertEqual(result, expected_value)
        self.assertEqual(mock_table_instance.dataset, self.mock_valid_dataset_details_instance)
    
    @patch("dataset_catalogue.models.fetch_data_from_api")
    def test_get_dataset_report_ids(self, mock_fetch_dataset_details_api_data):
        mock_fetch_dataset_details_api_data.return_value = {"reports": [{"id": "mock-report-id"}]}
        result = self.mock_valid_dataset_details_instance.get_dataset_report_ids(self.mock_valid_dataset_details_instance.url)
        self.assertEqual(result, ["mock-report-id"])
    
    @patch("dataset_catalogue.models.DatasetReport")
    def test_get_dataset_report_objects(self, MockDatasetReport):
        mock_report_instance = MagicMock()
        mock_report_instance.id = "mock-report-id"
        mock_report_instance.dataset = self.mock_valid_dataset_details_instance

        MockDatasetReport.return_value = mock_report_instance

        result = self.mock_valid_dataset_details_instance.get_dataset_report_objects(self.mock_valid_dataset_details_instance.report_ids)
        expected_value = [mock_report_instance]
        
        self.assertEqual(result, expected_value)
        self.assertEqual(mock_report_instance.dataset, self.mock_valid_dataset_details_instance)