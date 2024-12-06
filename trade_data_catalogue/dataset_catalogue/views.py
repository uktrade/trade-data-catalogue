from django.http import HttpResponse
from django.views.generic import TemplateView
from django.core.paginator import Paginator
import csv

from trade_data_catalogue.utils import BASE_API_URL
from trade_data_catalogue.utils import fetch_data_from_api

from .models import Dataset, DatasetDetails, DatasetDataPreview
from trade_data_catalogue.base import BaseBreadcrumbView


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


class DatasetDetailsView(BaseBreadcrumbView):
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
                table.set_csv_data(True)
                table.set_size_messsage()
            context["tables_page"] = tables_page

        if hasattr(dataset, "reports"):
            reports_paginator = Paginator(dataset.reports, 5)
            reports_page_number = self.request.GET.get("reports_page")
            reports_page = reports_paginator.get_page(reports_page_number)
            for report in reports_page:
                report.set_raw_csv_data()
                report.set_csv_data(True)
                report.set_size_messsage()
            context["reports_page"] = reports_page

        return context


class DatasetDataPreviewView(BaseBreadcrumbView):
    template_name = "dataset_catalogue/preview.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        dataset_id = kwargs.get("dataset_id")
        version = kwargs.get("version")
        data_type = kwargs.get("data_type")
        data_id = kwargs.get("data_id")

        dataset = DatasetDataPreview(dataset_id, version, data_type, data_id)

        rows_per_page = 20

        rows_paginator = Paginator(dataset.data_object.csv_rows, rows_per_page)
        rows_page_number = int(self.request.GET.get("rows_page", 1))
        rows_page = rows_paginator.get_page(rows_page_number)

        upper_rows_threshold = rows_per_page * rows_page_number
        lower_rows_threshold = upper_rows_threshold - (rows_per_page - 1)

        if len(rows_page) < rows_per_page:
            upper_rows_threshold = (lower_rows_threshold + len(rows_page)) - 1

        context["dataset"] = dataset

        if hasattr(dataset.data_object, "columns"):
            context["columns_metadata"] = dataset.data_object.columns

        context["data_type"] = data_type.title()
        context["data_headers"] = dataset.data_object.csv_headers
        context["row_count"] = dataset.data_object.csv_row_count
        context["rows_page"] = rows_page
        context["lower_rows_threshold"] = lower_rows_threshold
        context["upper_rows_threshold"] = upper_rows_threshold

        return context

    def download_csv(self, dataset_id, version, data_type, data_id):
        data_url = f"{BASE_API_URL}/v1/datasets/{dataset_id}/versions/{version}/{data_type}s/{data_id}/data?format=csv"

        fetched_csv_data = fetch_data_from_api(data_url, False, True)

        response = HttpResponse(fetched_csv_data, content_type="text/csv")
        response["Content-Disposition"] = (
            f'attachment; filename="{dataset_id}-{version}-{data_id}.csv"'
        )

        return response

    def get(self, request, *args, **kwargs):
        if "download" in request.GET:
            dataset_id = kwargs.get("dataset_id")
            version = kwargs.get("version")
            data_type = kwargs.get("data_type")
            data_id = kwargs.get("data_id")

            return self.download_csv(dataset_id, version, data_type, data_id)

        return super().get(request, *args, **kwargs)
