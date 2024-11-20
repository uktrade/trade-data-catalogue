from trade_data_catalogue.utils import BASE_API_URL
from trade_data_catalogue.utils import (
    fetch_data_from_api,
    get_transformed_string_from_pattern,
    read_and_parse_raw_csv_data,
)


class Dataset:
    def __init__(self, id):
        self.id = id
        self.url = f"{BASE_API_URL}/v1/datasets/{self.id}"
        self.title = self.get_formatted_dataset_title(self.id)
        self.versions = self.get_dataset_versions(f"{self.url}/versions?format=json")

    def get_formatted_dataset_title(self, dataset_id):
        dehyphenated_dataset_id = dataset_id.replace("-", " ")
        title_cased_dataset_id = dehyphenated_dataset_id.title()
        dataset_title_with_correct_region = get_transformed_string_from_pattern(
            title_cased_dataset_id, r"\b(Uk|Eu)\b"
        )

        return dataset_title_with_correct_region

    def get_dataset_versions(self, url):
        json_data = fetch_data_from_api(url)
        dataset_version_ids = json_data["versions"]
        dataset_versions = [version["id"] for version in dataset_version_ids]
        return dataset_versions

    def get_number_of_dataset_versions(self, versions):
        dataset_version_length = len(versions)
        return dataset_version_length

    def set_number_of_dataset_versions(self):
        self.versions_count = self.get_number_of_dataset_versions(self.versions)

    def get_version_count_message(self, versions_count):
        if versions_count > 1:
            return f"{versions_count} versions"
        return f"{versions_count} version"

    def set_version_count_message(self):
        self.version_count_message = self.get_version_count_message(self.versions_count)

    def get_latest_version(self, versions):
        if versions:
            latest_version = versions[0]
            return latest_version
        return None

    def set_latest_version(self):
        self.latest_version = self.get_latest_version(self.versions)


class DatasetDetails(Dataset):
    def __init__(self, id, version):
        super().__init__(id)
        self.version = version

    def get_dataset_metadata(self, url):
        csvw_data = fetch_data_from_api(url)
        if csvw_data is None:
            return None
        return csvw_data

    def set_dataset_metadata(self):
        self.metadata = self.get_dataset_metadata(
            f"{self.url}/versions/{self.version}/metadata?format=csvw"
        )

    def set_description(self):
        if "dc:description" in self.metadata:
            self.description = self.metadata["dc:description"]

    def get_dataset_table_ids(self, url):
        json_data = fetch_data_from_api(url)
        if "tables" in json_data:
            table_ids = json_data["tables"]
            dataset_table_ids = [table["id"] for table in table_ids]
            return dataset_table_ids
        return None

    def set_dataset_table_ids(self):
        self.table_ids = self.get_dataset_table_ids(
            f"{self.url}/versions/{self.version}/tables?format=json"
        )

    def set_dataset_tables(self, tables):
        self.tables = tables

    def get_dataset_report_ids(self, url):
        json_data = fetch_data_from_api(url)
        if "reports" in json_data:
            report_ids = json_data["reports"]
            dataset_report_ids = [report["id"] for report in report_ids]
            return dataset_report_ids
        return None

    def set_dataset_report_ids(self):
        self.report_ids = self.get_dataset_report_ids(
            f"{self.url}/versions/{self.version}/reports?format=json"
        )

    def set_dataset_reports(self, reports):
        self.reports = reports

    def set_dataset_versions(self):
        versions = self.get_dataset_versions(f"{self.url}/versions?format=json")
        self.versions = versions[0:20]


class BaseDatasetDataObject:
    def __init__(self, id, dataset):
        self.id = id
        self.dataset = dataset

    def get_raw_csv_data(self, url):
        csv_data = fetch_data_from_api(
            url,
            False,
            True,
        )
        return csv_data

    def set_raw_csv_data(self):
        self.raw_csv_data = self.get_raw_csv_data(self.data_url)

    def set_csv_data(self):
        self.csv_headers, self.csv_rows, self.csv_row_count = (
            read_and_parse_raw_csv_data(self.raw_csv_data)
        )

    def set_size_messsage(self):
        if self.csv_row_count < 2500:
            self.size = "Small"
        elif 2500 <= self.csv_row_count < 10000:
            self.size = "Medium"
        elif self.csv_row_count >= 10000:
            self.size = "Large"


class DatasetTable(BaseDatasetDataObject):
    def __init__(self, id, dataset):
        super().__init__(id, dataset)
        self.data_url = f"{self.dataset.url}/versions/{self.dataset.version}/tables/{self.id}/data?format=csv"


class DatasetReport(BaseDatasetDataObject):
    def __init__(self, id, dataset):
        super().__init__(id, dataset)
        self.data_url = f"{self.dataset.url}/versions/{self.dataset.version}/reports/{self.id}/data?format=csv"
