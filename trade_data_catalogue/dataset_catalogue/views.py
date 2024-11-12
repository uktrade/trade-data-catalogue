from django.shortcuts import render
from django.views.generic import TemplateView

from trade_data_catalogue.utils import BASE_API_URL
from trade_data_catalogue.utils import fetch_json_data_from_api

from .models import Dataset, DatasetDetails


class DatasetCatalogueView(TemplateView):
    fetch_url = f"{BASE_API_URL}/v1/datasets?format=json"
    template_name = "dataset_catalogue/catalogue.html"

    def get_dataset_ids(self, json_data):
        datasets = json_data["datasets"]
        dataset_ids = [dataset["id"] for dataset in datasets]

        return dataset_ids

    def get_dataset_objects(self, dataset_ids):
        datasets = {}
        for dataset_id in dataset_ids:
            this_dataset = Dataset(dataset_id)
            this_dataset.set_formatted_dataset_title()
            this_dataset.set_dataset_versions()
            this_dataset.set_number_of_dataset_versions()
            this_dataset.set_version_count_message()
            this_dataset.set_latest_version()
            datasets[dataset_id] = this_dataset

        return datasets

    def get(self, request):
        json_data = fetch_json_data_from_api(self.fetch_url)
        dataset_ids = self.get_dataset_ids(json_data)
        datasets = self.get_dataset_objects(dataset_ids)

        dataset_count = len(datasets)

        return render(
            request,
            self.template_name,
            {"datasets": datasets, "dataset_count": dataset_count},
        )


class DatasetDetailView(TemplateView):
    template_name = "dataset_catalogue/details.html"

    def get_dataset_detail_object(self, dataset_id, version):
        dataset_details = DatasetDetails(dataset_id, version)
        dataset_details.set_formatted_dataset_title()
        dataset_details.set_dataset_metadata()
        dataset_details.set_description()

        return dataset_details

    def get(self, request, dataset_id, version):
        dataset = self.get_dataset_detail_object(dataset_id, version)

        return render(request, self.template_name, {"dataset": dataset})
