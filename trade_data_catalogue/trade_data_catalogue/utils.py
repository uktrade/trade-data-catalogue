import requests, re, csv


BASE_API_URL = "https://data.api.trade.gov.uk"


def fetch_data_from_api(url, as_json=True, stream=False):
    response = requests.get(url, stream=stream)

    if response.status_code == 200:
        if as_json:
            return response.json()
        return response
    else:
        return {"error": "Failed to fetch data"}


def read_and_parse_raw_csv_data(response_data):
    csv_reader = csv.reader(response_data.iter_lines(decode_unicode=True))

    headers = next(csv_reader)
    rows = []
    row_count = 0

    for row in csv_reader:
        if row_count == 10000:
            break
        row_count += 1
        rows.append(row)

    return headers, rows, row_count


def get_transformed_string_from_pattern(string, pattern):
    return re.sub(pattern, lambda match: match.group(0).upper(), string)
