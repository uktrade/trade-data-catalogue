import requests


def fetch_json_data_from_api(url):
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to fetch data"}
