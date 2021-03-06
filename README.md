# ph-earthquake-dashboard
An unofficial web app/service that scrapes and parses [Phivolcs DOST Earthquake Information](https://earthquake.phivolcs.dost.gov.ph/) bulletins, making the data searchable via REST API endpoints.

## Features
Once completed, this project will include:
* Scrapy spider that collects current and historic earthquake information from Phivolcs DOST bulletins
* Postgres database backend
* Periodic tasks to run scraping jobs with Celery and Redis
* API endpoints to access stored earthquake data using Django REST [to be implemented]
* Service deployed as multi-container Docker app [to be implemented]

## License<a name="license"></a>
[MIT license](https://opensource.org/licenses/MIT)