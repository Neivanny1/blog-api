## Blogging Website using Flask

RESTful webservice created using Python Flask and SQLite for a Blogging website.

## Setting up postgres db
CREATE DATABASE mydatabase; <br>
CREATE USER myuser WITH PASSWORD 'mypassword'; <br>
GRANT ALL PRIVILEGES ON DATABASE mydatabase TO myuser; <br>
## Setting up mysql db
GRANT ALL PRIVILEGES ON DATABASE blog_api TO dev;
## ## Setting up Mongo db

### Installation Requirements (libraries)

  1. ```pip install Flask```
  2. ```pip install Flask-SQLAlchemy```

### Web Application

<div align='center'>
<img src = 'templates/website.JPG' height="400px">
</div>

### Steps of Code Execution

  1. Clone / Download this [repository](https://github.com/nikita9604/Automated-Voice-Controlled-Email-Sender)
  2. Unzip the downloaded folder
  3. Open any python editor (Here, [VS Code](https://code.visualstudio.com/) is used)
  4. Run this [python file](https://github.com/nikita9604/Blogging-Website-using-Flask/blob/main/app.py) and go to the link to execute the application.

### References

https://www.tutorialspoint.com/flask/index.htm
https://flask-restful.readthedocs.io/en/latest/


flask db init
flask db migrate -m "description of migration"
flask db upgrade
flask run
