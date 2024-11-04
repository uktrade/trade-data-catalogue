from django.http import JsonResponse
from django.views import View

from trade_data_catalogue.utils import fetch_json_data_from_api


class DatasetCatalogueView(View):
    fetch_url = "https://data.api.trade.gov.uk/v1/datasets?format=json"

    def get_all_datasets(self):
        return fetch_json_data_from_api(self.fetch_url)

    def get(self, request):
        all_datasets = self.get_all_datasets()
        return JsonResponse(all_datasets)
