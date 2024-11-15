from django.views.generic import TemplateView
from django.core.paginator import Paginator

from trade_data_catalogue.utils import BASE_API_URL
from trade_data_catalogue.utils import fetch_data_from_api

from .models import Dataset, DatasetDetails, DatasetTable, DatasetReport


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        json_data = fetch_data_from_api(self.fetch_url)
        dataset_ids = self.get_dataset_ids(json_data)
        datasets = self.get_dataset_objects(dataset_ids)

        context["datasets"] = datasets
        context["dataset_count"] = len(datasets)

        return context


class DatasetDetailView(TemplateView):
    template_name = "dataset_catalogue/details.html"

    def get_dataset_details_object(self, dataset_id, version):
        dataset_details = DatasetDetails(dataset_id, version)
        dataset_details.set_formatted_dataset_title()
        dataset_details = self.initialise_dataset_details_metadata(dataset_details)
        dataset_details.set_dataset_table_ids()
        dataset_details.set_dataset_report_ids()

        if dataset_details.table_ids != None:
            dataset_details = self.get_dataset_table_objects(dataset_details)
        if dataset_details.report_ids != None:
            dataset_details = self.get_dataset_report_objects(dataset_details)

        dataset_details.set_dataset_versions()
        dataset_details.set_latest_version()

        return dataset_details

    def initialise_dataset_details_metadata(self, dataset_details):
        dataset_details.set_dataset_metadata()
        if dataset_details.metadata != None:
            dataset_details.set_description()

        return dataset_details

    def get_dataset_table_objects(self, dataset_details):
        dataset_tables = []
        for table_id in dataset_details.table_ids:
            this_dataset_table = DatasetTable(table_id)
            dataset_tables.append(this_dataset_table)
        dataset_details.set_dataset_tables(dataset_tables)

        return dataset_details

    def get_dataset_report_objects(self, dataset_details):
        dataset_reports = []
        for report_id in dataset_details.report_ids:
            this_dataset_report = DatasetReport(report_id)
            dataset_reports.append(this_dataset_report)
        dataset_details.set_dataset_reports(dataset_reports)

        return dataset_details
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        dataset = self.get_dataset_details_object(**kwargs)
        context["dataset"] = dataset

        if hasattr(dataset, "tables"):
            tables_paginator = Paginator(dataset.tables, 5)
            tables_page_number = self.request.GET.get("tables_page")
            tables_page = tables_paginator.get_page(tables_page_number)
            context["tables_page"] = tables_page

        # if hasattr(dataset, "reports"):
        #     reports_paginator = Paginator(dataset.reports, 5)
        #     reports_page_number = request.GET.get("reports_page")
        #     reports_page = reports_paginator.get_page(reports_page_number)
        #     context["reports_page"] = reports_page

        return context
