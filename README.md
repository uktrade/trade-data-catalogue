# trade-data-catalogue
An open source data platform for viewing data provided by the DBT Public Data API

- Does not use a database
- Data can be accessed by an API, or downloaded
- Promotes immutable and versioned datasets
- Includes [GOV.UK Design System](https://design-system.service.gov.uk/)-styled documentation and frontend
- Low memory usage even for large datasets - responses are streamed to the client
- [HTTP Range requests](https://developer.mozilla.org/en-US/docs/Web/HTTP/Range_requests) are supported when possible to allow clients to resume interrupted downloads
- [HTTP Cookies](https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies) are not used
