import requests, re


BASE_API_URL = "https://data.api.trade.gov.uk"


def fetch_data_from_api(url):
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to fetch data"}


def get_transformed_string_from_pattern(string, pattern):
    return re.sub(pattern, lambda match: match.group(0).upper(), string)
