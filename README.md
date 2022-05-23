# Installation

Requires [Docker](https://www.docker.com/) to run.

Clone the repository and start docker.

## First way

```sh
cd BigProfiles-test\bin
.\start.sh
```

## Second way

```sh
cd BigProfiles-test
docker-compose up
```

Verify the deployment by navigating to your server address in
your preferred browser.

```sh
http://localhost:8000
```

## Authentication

You have to pass the an API key parameter within the header of the request:
  - key: x-api-key
  - value: BigProfiles-API

## Commands

Add data to db:

```sh
http://localhost:8000/ingestion
```
Example body:
```sh
{
"payload" : "test payload",
"key": 6
}
```
Retrieve data from db:

```sh
http://localhost:8000/retrieve?date_from=2022-05-23 10:10:00&date_to=2022-05-23 10:12:00
```

## Stop

```sh
cd BigProfiles-test\bin
.\stop.sh
```

