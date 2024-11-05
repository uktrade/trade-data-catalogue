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

    def get_formatted_dataset_title(self, dataset_id):
        dehyphenated_dataset_id =  dataset_id.replace('-', ' ')
        title_cased_dataset_id = dehyphenated_dataset_id.title()
        return title_cased_dataset_id

    def get(self, request):
        dataset_ids = self.get_dataset_ids()
        datasets = {}
        for dataset_id in dataset_ids:
            datasets[dataset_id] = self.get_formatted_dataset_title(dataset_id)
        return render(request, self.template_name, {"datasets": datasets})
