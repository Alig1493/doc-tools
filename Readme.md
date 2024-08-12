# PDF DOC-TOOLS IO

* Project to allow operations on pdf
* Allow merge, compress pdfs
* Integrate with google drive
* Allow to browse select google drive folders and save locations

## Pre-requisites:
* pip-tools
* Docker (now comes with docker compose)
* pre-commit

## Running pytest:
* `docker compose run testrunner`

## Running locust performance test:
* Start the web server, locust master and worker nodes with this command:
    `docker compose up web locust_master locust_worker --scale locust_worker=4`
* Go to the web browser and open: `0.0.0.0:8089` and enter the configurations to start your performance test, the attack host should be: `http://web:8000`
