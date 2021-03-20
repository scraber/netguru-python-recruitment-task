# Netguru python recruitment task

Netguru python recruitment task is a simple REST API of basic cars makes and models written in Django with usage of external API

---
# Run Locally

### Clone the source 

```sh
git clone https://github.com/scraber/netguru-python-recruitment-task.git
cd netguru-python-recruitment-task
```


## Using Docker
### Make sure you have installed both docker and docker-compose

1. Install [`docker`](https://docs.docker.com/get-docker/).
2. Install [`docker-compose`](https://docs.docker.com/compose/install/).
3. Create .env file for system variables (replace fields within <> with own values)
```
DEBUG=0
SECRET_KEY=<secret_key>
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 0.0.0.0 [::1]
SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=<postgres>
SQL_USER=<user>
SQL_PASSWORD=<password>
SQL_HOST=db
SQL_PORT=<port>
```
4. Create .env.db file for system variables (replace fields within <> with own values)
```
POSTGRES_USER=<user>
POSTGRES_PASSWORD=<password>
POSTGRES_DB=<db_name>
```


Use docker-compose to build 
```sh
docker-compose -f docker-compose.prod.yml up -d --build  
```
Run initial migrations 
```sh
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate --noinput
```
Create Django superuser (which you can use for token auth, later on)
```sh
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
```

### Run tests
```sh
docker-compose -f docker-compose.prod.yml exec web python manage.py test
```

# Usage - available endpoints
API uses Token Authentication, you can get token using test user credentials from
>POST /api-token-auth/
```json
{
    "username": "test",
    "password": "12test34"
}
```

Pass received token into HTTPHeader for each request, for example:
>Authorization: Bearer <received_token>

---

>POST /cars
```json
{
    "make_name": "Tesla",
    "model_name": "Model S"
}
```

>POST /rate
* Add a rate for a car (id) from 1 to 5
```json
{
    "car": 1,
    "rating": 1
}
```

>GET /cars
* Fetches list of cars present in database with their current average rate

>GET /popular
* Returns top cars present in the database based on number of rates

