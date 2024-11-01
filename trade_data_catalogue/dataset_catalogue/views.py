from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import View 
import requests


class DatasetCatalogueView(View):
    def dataset_catalogue_view(request):
        response = requests.get('https://data.api.trade.gov.uk/v1/datasets?format=json')
    
        if response.status_code == 200:
            data = response.json()
            return JsonResponse(data)
        else:
            return JsonResponse({'error': 'Failed to fetch data'})