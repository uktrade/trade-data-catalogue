from django.test import TestCase
from ...views import DatasetCatalogueView


class TestDatasetCatalogueView(TestCase):
    def setUp(self):
        self.view = DatasetCatalogueView()

    def test_view_is_instance_of_class(self):
        self.assertIsInstance(self.view, DatasetCatalogueView)
