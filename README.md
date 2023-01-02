## foodgram-project-react
Application "Product Assistant": a site, on applications you can publish recipes, add other people's recipes to your favorites and subscribe to publications of other authors. The Shopping List service allows users to create a list of products that are needed to prepare selected dishes.

## Run the project
### Clone repository to your computer:

HTTPS - https://github.com/ShotelYa/foodgram-project-react

### Create and feel the .env file
```
DB_ENGINE=<...> # specify that we work with postgresql data base
DB_NAME=<...> # data base name
POSTGRES_USER=<...> # login for connecting to data base
POSTGRES_PASSWORD=<...> # password for connection to data base (create your own)
DB_HOST=<...> # name of the servise (container)
DB_PORT=<...> # port for conection to data base
SECRET_KEY=<...> # kay from settings.py
```

1.Assembly and run the container

sudo docker compose up -d --build --force-recreate
```
2.Migrations

sudo docker compose exec backend python manage.py makemigrations
sudo docker compose exec backend python manage.py migrate
```
3.Create a Django superuser

sudo docker compose exec backend python manage.py createsuperuser
```
4.Collect static

sudo docker compose exec backend python manage.py collectstatic --no-input
```
5.Load data to database

sudo docker compose exec backend python manage.py load-data

Redoc:
http://185.72.246.211/redoc/
***
### Example of API request:

Request for recipes:
```python
import requests
from pprint import pprint
url = 'http://127.0.0.1/api/recipes/'
request = requests.get(url).json()
pprint(request)
```

## Technology

- Python 3
- Django
- Django REST Framework
- Simple JWT
- Docker
- PostgresSQL
- Nginx
- Gunicorn
