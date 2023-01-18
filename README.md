# Travel Diary
Django web application that allows users to store their travel memories on a map.

![image](https://user-images.githubusercontent.com/91879429/194930241-e97f70b1-bfe3-4be5-8c8c-64203ea25a9f.png)

## Table of contents
* [Key features](#key-features)
* [Technology](#technology)
* [Setup](#setup-and-run)

### Key features
* User registration, login and profile creation.

![image](https://user-images.githubusercontent.com/91879429/194930246-286bc528-f7b0-41d8-a99f-337bf7b9732c.png)

![image](https://user-images.githubusercontent.com/91879429/194930234-a4ebc50e-50fc-459d-8c8c-c7da466eb1b1.png)

![image](https://user-images.githubusercontent.com/91879429/194930238-9c0893c7-9e3d-4aff-a401-af47e3a634b4.png)

* Adding markers to the map with additional information about the journey: location, date, description and photo.

![image](https://user-images.githubusercontent.com/91879429/194931281-c0a6a6f6-2737-404e-9cf8-4e9baf645685.png)

* Map view with all added markers.

![image](https://user-images.githubusercontent.com/91879429/194930245-f45b8fea-2662-423d-b1a2-9a7b405991fe.png)

* Photo gallery.

![image](https://user-images.githubusercontent.com/91879429/194930230-b2c55648-63f3-4ce4-89d7-de2a8981db2a.png)

* Update, Delete - manage markers.

![image](https://user-images.githubusercontent.com/91879429/194930236-cf0baf97-6ef2-4e34-b33e-7018de723434.png)

### Technology
* Python 3.10
* Django 4.1
* PostgreSQL
* Folium 0.12.1
* HTML5/CSS3
* Bootstrap 5


### Setup and Run 
You need to have installed:
* Python 3.10
* PostgreSQL
* Docker *

1. Clone or download the repo.
2. Create a virtual environment and activate it.
3. Connect to the database.
4. From your command line pointing to the project root directory:
```bash
# Install requirements:
$ pip install -r requirements.txt

# Migrate tables:
$ python manage.py migrate

# Run server:
$ python manage.py runserver
```

*Using Docker:
1. Clone or download the repo.

2. From your command line pointing to the project root directory:
```bash
# Build an image:
$ docker build -t traveldiary .

# Start the container:
$ docker compose up
```

You are now able to access `localhost:8000` in your browser.