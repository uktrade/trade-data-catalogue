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
        dataset_version_length = len(dataset_versions)
        return dataset_version_length

    def set_dataset_versions(self):
        self.versions = self.get_dataset_versions(f"{self.url}/versions?format=json")
