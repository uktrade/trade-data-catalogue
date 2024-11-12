from trade_data_catalogue.utils import BASE_API_URL
from trade_data_catalogue.utils import fetch_json_data_from_api


class Dataset:
    def __init__(self, id):
        self.id = id
        self.url = f"{BASE_API_URL}/v1/datasets/{self.id}"

    def get_formatted_dataset_title(self, dataset_id):
        dehyphenated_dataset_id = dataset_id.replace("-", " ")
        title_cased_dataset_id = dehyphenated_dataset_id.title()
        return title_cased_dataset_id

    def set_formatted_dataset_title(self):
        self.title = self.get_formatted_dataset_title(self.id)

    def get_dataset_versions(self, url):
        json_data = fetch_json_data_from_api(url)
        dataset_version_ids = json_data["versions"]
        dataset_versions = [version["id"] for version in dataset_version_ids]
        return dataset_versions

    def set_dataset_versions(self):
        self.versions = self.get_dataset_versions(f"{self.url}/versions?format=json")

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
        latest_version = versions[0]
        return latest_version

    def set_latest_version(self):
        self.latest_version = self.get_latest_version(self.versions)


class DatasetDetails(Dataset):
    def __init__(self, id, version):
        super().__init__(id)
        self.version = version

    def get_dataset_metadata(self, url):
        json_data = fetch_json_data_from_api(url)
        if json_data is None:
            return None
        return json_data

    def set_dataset_metadata(self):
        self.metadata = self.get_dataset_metadata(
            f"{self.url}/versions/{self.version}/metadata?format=csvw"
        )

    def set_description(self):
        if "dit:databases" in self.metadata:
            self.description = self.metadata["dit:databases"][0]["dc:title"]
