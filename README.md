# Travel Diary
Django web application that allows users to store their travel memories on a map. 

## Table of contents
* [Key features](#key-features)
* [Technology](#technology)
* [Setup](#setup)
* [Run server](#run-server)

### Key features
* User registration, login and profile creation.
* Adding markers to the map with additional information about the journey: location, date, description and photo.
* Map view with all added markers.


### Technology
* Python 3.10
* Django 4.1
* PostgreSQL 13.0 + postGIS 3.0
* Folium 0.12.1
* HTML5/CSS3
* Bootstrap 5


### Setup
You need to have installed:
* Python 3.10
* PostgreSQL 13.0 + postGIS 3.0 extension

You can use Docker to get Postgres database with PostGIS extensions.
Make sure you have Docker installed and type the following command:
```bash
docker run --name=postgis -d -e POSTGRES_USER=user001 -e POSTGRES_PASS=secret1234 -e POSTGRES_DBNAME=gis -p 5432:5432 -v $(pwd)/postgres_data:/var/lib/postgresql kartoza/postgis:13
```


1. Clone or download the repo.

2. Create a virtual environment and activate it.

3. Connect to the database.

From your command line pointing to the project root directory:
```bash
# Install requirements
$ pip install -r requirements.txt

# Migrate tabels
$ python manage.py migrate
```

### Run Server
To run server open command line pointing to the project root directory:

```bash
python manage.py runserver
```

You are now able to access `localhost:8000` in your browser.
