# trade-data-catalogue
An open source data platform for viewing data provided by the DBT Public Data API

- Does not use a database
- Data can be accessed by an API, or downloaded
- Promotes immutable and versioned datasets
- Includes GOV.UK Design System-styled documentation and frontend
- Low memory usage even for large datasets - responses are streamed to the client
- HTTP Range requests are supported when possible to allow clients to resume interrupted downloads
- HTTP Cookies are not used
