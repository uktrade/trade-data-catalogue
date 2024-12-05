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
        self.versions = self.get_all_dataset_versions(
            f"{self.url}/versions?format=json"
        )

        if self.versions:
            self.versions_count = self.get_number_of_dataset_versions(self.versions)
            self.version_count_message = self.get_version_count_message(
                self.versions_count
            )
            self.latest_version = self.get_latest_version(self.versions)

    def get_formatted_dataset_title(self, dataset_id):
        dehyphenated_dataset_id = dataset_id.replace("-", " ").replace(".", " ")
        title_cased_dataset_id = dehyphenated_dataset_id.title()
        dataset_title_with_correct_region = get_transformed_string_from_pattern(
            title_cased_dataset_id, r"\b(Uk|Eu)\b"
        )
        dataset_title_with_correct_id_capitalisation = (
            get_transformed_string_from_pattern(
                dataset_title_with_correct_region, r"\b[iI][dD]\b"
            )
        )
        return dataset_title_with_correct_id_capitalisation

    def get_all_dataset_versions(self, url):
        json_data = fetch_data_from_api(url)
        dataset_version_ids = json_data["versions"]
        dataset_versions = [version["id"] for version in dataset_version_ids]
        return dataset_versions

    def get_number_of_dataset_versions(self, versions):
        dataset_version_length = len(versions)
        return dataset_version_length

    def get_version_count_message(self, versions_count):
        if versions_count > 1:
            return f"{versions_count} versions"
        return f"{versions_count} version"

    def get_latest_version(self, versions):
        if versions:
            latest_version = versions[0]
            return latest_version
        return None


class DatasetDetails(Dataset):
    def __init__(self, id, version):
        super().__init__(id)
        self.version = version
        self.metadata = self.get_dataset_metadata(
            f"{self.url}/versions/{self.version}/metadata?format=csvw"
        )

        if "dc:description" in self.metadata:
            self.description = self.metadata["dc:description"]

        self.table_ids = self.get_dataset_table_ids(
            f"{self.url}/versions/{self.version}/tables?format=json"
        )
        self.report_ids = self.get_dataset_report_ids(
            f"{self.url}/versions/{self.version}/reports?format=json"
        )

        if self.table_ids:
            self.tables = self.get_dataset_table_objects(self.table_ids)
        if self.report_ids:
            self.reports = self.get_dataset_report_objects(self.report_ids)

        self.versions = self.versions[0:20]

    def get_dataset_metadata(self, url):
        csvw_data = fetch_data_from_api(url)
        if csvw_data is None:
            return None
        return csvw_data

    def get_dataset_table_ids(self, url):
        json_data = fetch_data_from_api(url)
        if "tables" in json_data:
            table_ids = json_data["tables"]
            dataset_table_ids = [table["id"] for table in table_ids]
            return dataset_table_ids
        return None

    def get_dataset_table_objects(self, table_ids):
        dataset_tables = []
        for table_id in table_ids:
            this_dataset_table = DatasetTable(table_id, self)
            dataset_tables.append(this_dataset_table)
        return dataset_tables

    def get_dataset_report_ids(self, url):
        json_data = fetch_data_from_api(url)
        if "reports" in json_data:
            report_ids = json_data["reports"]
            dataset_report_ids = [report["id"] for report in report_ids]
            return dataset_report_ids
        return None

    def get_dataset_report_objects(self, report_ids):
        dataset_reports = []
        for report_id in report_ids:
            this_dataset_report = DatasetReport(report_id, self)
            dataset_reports.append(this_dataset_report)
        return dataset_reports


class BaseDatasetDataObject:
    def __init__(self, id, dataset):
        self.id = id
        self.dataset = dataset
        self.title = self.get_formatted_data_object_title(self.id)

    def get_raw_csv_data(self, url):
        csv_data = fetch_data_from_api(
            url,
            False,
            True,
        )
        return csv_data

    def set_raw_csv_data(self):
        self.raw_csv_data = self.get_raw_csv_data(self.data_url)

    def set_csv_data(self, limit_rows):
        self.csv_headers, self.csv_rows, self.csv_row_count = (
            read_and_parse_raw_csv_data(self.raw_csv_data, limit_rows=limit_rows)
        )

    def set_size_messsage(self):
        if self.csv_row_count < 2500:
            self.size = "Small"
        elif 2500 <= self.csv_row_count < 10000:
            self.size = "Medium"
        elif self.csv_row_count >= 10000:
            self.size = "Large"

    def set_column_metadata(self, tables_metadata):
        columns = []
        for table in tables_metadata:
            if self.id in table["url"]:
                self.subtitle = table["dc:title"]
                for column in table["tableSchema"]["columns"]:
                    this_column = Column(column["name"], column["dc:description"])
                    columns.append(this_column)
                break
        if columns != None:
            self.columns = columns

    def get_formatted_data_object_title(self, data_object_id):
        dehyphenated_data_object_id = data_object_id.replace("-", " ").replace(".", " ")
        title_cased_data_object_id = dehyphenated_data_object_id.title()
        data_object_title_with_correct_region = get_transformed_string_from_pattern(
            title_cased_data_object_id, r"\b(Uk|Eu)\b"
        )
        data_object_with_correct_id_capitalisation = (
            get_transformed_string_from_pattern(
                data_object_title_with_correct_region, r"\b[iI][dD]\b"
            )
        )
        return data_object_with_correct_id_capitalisation


class Column:
    def __init__(self, name, description):
        self.name = name
        self.description = description


class DatasetTable(BaseDatasetDataObject):
    def __init__(self, id, dataset):
        super().__init__(id, dataset)
        self.data_url = f"{self.dataset.url}/versions/{self.dataset.version}/tables/{self.id}/data?format=csv"


class DatasetReport(BaseDatasetDataObject):
    def __init__(self, id, dataset):
        super().__init__(id, dataset)
        self.data_url = f"{self.dataset.url}/versions/{self.dataset.version}/reports/{self.id}/data?format=csv"


class DatasetDataPreview(Dataset):
    def __init__(self, id, version, data_type, data_id):
        super().__init__(id)

        self.version = version
        self.data_type = data_type
        self.data_id = data_id
        self.metadata = self.get_dataset_metadata(
            f"{self.url}/versions/{self.version}/metadata?format=csvw"
        )
        self.data_object = self.get_dataset_data_object(self.data_id, self.data_type)

        if "tables" in self.metadata:
            self.tables_metadata = self.metadata["tables"]
            self.data_object.set_column_metadata(self.tables_metadata)

    def get_dataset_data_object(self, data_id, data_type):
        if data_type == "table":
            data_object = DatasetTable(data_id, self)
        if data_type == "report":
            data_object = DatasetReport(data_id, self)

        data_object.set_raw_csv_data()
        data_object.set_csv_data(False)
        return data_object

    def get_dataset_metadata(self, url):
        csvw_data = fetch_data_from_api(url)
        if csvw_data is None:
            return None
        return csvw_data
