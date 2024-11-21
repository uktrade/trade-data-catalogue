from django.views.generic import TemplateView
from django.core.paginator import Paginator

from trade_data_catalogue.utils import BASE_API_URL
from trade_data_catalogue.utils import fetch_data_from_api

from .models import Dataset, DatasetDetails
from trade_data_catalogue.base import DatasetVersionBreadcrumbView


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
            if not this_dataset.versions:
                continue
            datasets[dataset_id] = this_dataset

        return datasets

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        json_data = fetch_data_from_api(self.fetch_url)
        dataset_ids = self.get_dataset_ids(json_data)
        datasets = self.get_dataset_objects(dataset_ids)

        context["datasets"] = datasets
        context["dataset_count"] = len(datasets)

        return context


class DatasetDetailsView(DatasetVersionBreadcrumbView):
    template_name = "dataset_catalogue/details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        dataset_id = kwargs.get("dataset_id")
        version = kwargs.get("version")

        dataset = DatasetDetails(dataset_id, version)
        context["dataset"] = dataset

        if hasattr(dataset, "tables"):
            tables_paginator = Paginator(dataset.tables, 5)
            tables_page_number = self.request.GET.get("tables_page")
            tables_page = tables_paginator.get_page(tables_page_number)
            for table in tables_page:
                table.set_raw_csv_data()
                table.set_csv_data()
                table.set_size_messsage()
            context["tables_page"] = tables_page

        if hasattr(dataset, "reports"):
            reports_paginator = Paginator(dataset.reports, 5)
            reports_page_number = self.request.GET.get("reports_page")
            reports_page = reports_paginator.get_page(reports_page_number)
            for report in reports_page:
                report.set_raw_csv_data()
                report.set_csv_data()
                report.set_size_messsage()
            context["reports_page"] = reports_page

        return context
