POST http://localhost:8000/api/hashrequests/ - create a new task, need auth via Basic Auth
GET http://localhost:8000/api/hashrequests/ - get list of all tasks

POST http://localhost:8000/api/users/ - create new user
body: x-www-form-urlencoded

- username: newuser
- password: newpass

GET http://localhost:8000/api/users/ - lists users

## to install

To prepare django to launch

```
python manage.py makemigrations
python manage.py migrate
```

Building and Running with Docker

```
docker-compose build
docker-compose up
```
