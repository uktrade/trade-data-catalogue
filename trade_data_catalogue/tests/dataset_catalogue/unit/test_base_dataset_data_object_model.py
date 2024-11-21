from django.test import TestCase

from dataset_catalogue.models import BaseDatasetDataObject

class TestBaseDatasetDataObject(TestCase):
    def test_set_size_message_returns_small(self):
        dataset_data_object = BaseDatasetDataObject(id="test-case", dataset={})
        dataset_data_object.csv_row_count = 1500
        dataset_data_object.set_size_messsage()

        result = dataset_data_object.size
        expected_value = "Small"
        
        self.assertEqual(result, expected_value)
    
    def test_set_size_message_returns_medium(self):
        dataset_data_object = BaseDatasetDataObject(id="test-case", dataset={})
        dataset_data_object.csv_row_count = 5000
        dataset_data_object.set_size_messsage()

        result = dataset_data_object.size
        expected_value = "Medium"
        
        self.assertEqual(result, expected_value)
    
    def test_set_size_message_returns_large(self):
        dataset_data_object = BaseDatasetDataObject(id="test-case", dataset={})
        dataset_data_object.csv_row_count = 11000
        dataset_data_object.set_size_messsage()

        result = dataset_data_object.size
        expected_value = "Large"
        
        self.assertEqual(result, expected_value)
    