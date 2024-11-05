from django.shortcuts import render
from django.views.generic import TemplateView

from trade_data_catalogue.utils import fetch_json_data_from_api


class DatasetCatalogueView(TemplateView):
    fetch_url = "https://data.api.trade.gov.uk/v1/datasets?format=json"
    template_name = "dataset_catalogue/catalogue.html"

    def get_all_datasets(self):
        return fetch_json_data_from_api(self.fetch_url)

    def get(self, request):
        all_datasets = self.get_all_datasets()
        print(all_datasets)
        return render(request, self.template_name, {"datasets": all_datasets})
