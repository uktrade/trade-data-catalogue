# trade-data-catalogue [![CircleCI](https://dl.circleci.com/status-badge/img/gh/uktrade/trade-data-catalogue/tree/main.svg?style=svg)](https://dl.circleci.com/status-badge/redirect/gh/uktrade/trade-data-catalogue/tree/main)
An open source data platform for viewing data provided by the DBT Public Data API

- Does not use a database
- Data can be accessed by an API, or downloaded
- Promotes immutable and versioned datasets
- Includes [GOV.UK Design System](https://design-system.service.gov.uk/)-styled documentation and frontend
- Low memory usage even for large datasets - responses are streamed to the client
- [HTTP Range requests](https://developer.mozilla.org/en-US/docs/Web/HTTP/Range_requests) are supported when possible to allow clients to resume interrupted downloads
- [HTTP Cookies](https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies) are not used


## Prerequisites

1. Python: Ensure Python 3.10 or higher is installed.
   
2. pip: Python's package manager.

3. Node.js & npm: For JavaScript dependencies (required by the [GOV.UK Design System](https://design-system.service.gov.uk/)).
   


## Setup

1. Clone the repository:
   
   `git clone https://github.com/uktrade/trade-data-catalogue.git`
   
2. Setup the virtual environment:

    `python -m venv venv`
   
     `source venv/bin/activate`
   
3. Install Python dependencies:

   `pip install -r requirements.txt`

4. Copy `sample.env` into `.env`:

   `cp sample.env .env`

5. Install frontend dependencies:

   `npm install`

6. Run on local server:

   `cd trade_data_catalogue`

   `python manage.py runserver`

