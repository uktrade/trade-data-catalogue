from django.shortcuts import render
from django.views.generic import TemplateView

from trade_data_catalogue.utils import fetch_json_data_from_api


class DatasetCatalogueView(TemplateView):
    fetch_url = "https://data.api.trade.gov.uk/v1/datasets?format=json"
    template_name = "dataset_catalogue/catalogue.html"

    def get_dataset_ids(self):
        json_data = fetch_json_data_from_api(self.fetch_url)
        datasets = json_data["datasets"]
        dataset_ids = [dataset["id"] for dataset in datasets]
        return dataset_ids

    def get(self, request):
        dataset_ids = self.get_dataset_ids()
        print(dataset_ids)
        return render(request, self.template_name, {"dataset_ids": dataset_ids})
