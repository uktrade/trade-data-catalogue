from django.test import TestCase
from django.urls import reverse

from dataset_catalogue.views import DatasetDetailView


class TestDatasetDetailView(TestCase):
    def setUp(self):
        self.view = DatasetDetailView()

    def test_view_is_instance_of_class(self):
        self.assertIsInstance(self.view, DatasetDetailView)
