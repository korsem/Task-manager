# Task-manager
<h3> Backend for the basic CRUD app using Django Rest with PostgreSQL. </h3>

## Requirements 
* Python 
* Django 
* Django Rest framework
* PostgreSQL

## Installation
1) Clone the repository 
```
git clone https://github.com/korsem/Task-manager.git
```
2) Enter the folder with repository and create a virtual environment
```
python -m venv env
```
3) Install all the required dependencies
```
pip install -r requirements.txt
```
## Launching the database

1) Configure the database settings in 'settings.py'
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_database_name',
        'USER': 'your_username',
        'PASSWORD': 'your_database_password',
        'HOST': 'your_host',
        'PORT': 'your_port',
    }
}
```
Where in "your ..." write the data for your database
you can do it by creating '.env' file (recommended) like this:
```
touch .env
```
to create .env file
Then fill your .env file like this:
```
DB_NAME=your_database_name
DB_USER=your_username
DB_PASSWORD=your_database_password
DB_HOST=your_host
DB_PORT=your_port
```
2) Perform database migrations
```
python manage.py migrate
```
## Starting the server
1) Run server by
```
python manage.py runserver
```
2) Open the app
```
http://127.0.0.1:8000/
```

## Use
* By adding a certain endpoint you get a certain functionality:

| Endpoint                              | HTTP Method | Result                                     |
|---------------------------------------|-------------|--------------------------------------------|
| `tasks/api`                           | GET         | Get all tasks                              |
| `tasks/api`                           | POST        | Create a new task                          |
| `tasks/api/:id`                       | GET         | Get a certain task by id                   |
| `tasks/api/:task_id`                  | DELETE      | Delete a task                              |
| `tasks/api/:task_id`                  | PUT         | Modify all fields except id                |
| `tasks/api/:task_id`                  | PATCH       | Modify choosen fields                      |
| `tasks/api/users`                     | GET         | List all users                             |
| `tasks/api/usrs/:user_id`             | GET          | Get a certain user by id                   |
| `tasks/api/search/*keyword*/`         | GET          | Filter the tasks by a keyword              |
| `tasks/api/search/*field*/*keyword*/` | GET          | Filter the tasks by a keyword in a field   |
| `tasks/api/history/:task_id/`         | GET          | Get a history of changes in a certain task |

* To use POST/PATCH/PUT function you write in the content field as follows:
```
{
 "name": "your_task_name",
 "description": "your_description",
 "status": "your_status",
 "assigned_to": "user_id_to_be_assigned"
}
```
Where from these fields only name is obligatory, if not filled assigned_to and description fields are set to null and status set to 'Nowy'

## What I plan to add
* user login/sign in system
* permissions and authentications
* curl instruction