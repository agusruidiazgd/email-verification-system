# email-verification-system
This is a example of CRUD and mail verification system.
Technologies:

- Python / Flask
- PostgreSQL
- SMPT Gmail

**🌱Create the schema**
PostgreSQL

- Create table users:

```sql
CREATE TABLE users (
    id serial PRIMARY KEY,
    username VARCHAR ( 40 ) NOT NULL,
    email VARCHAR ( 40 ) NOT NULL UNIQUE, 
    is_verified BOOLEAN NOT NULL DEFAULT false,
    key VARCHAR ( 90 ) NOT NULL DEFAULT '""'
);
```
Check that all tables were created:

```sql
describe tables;
```

**🌿Install Project**

Open the terminal and follow these steps.

```
$ git clone https://github.com/agusruidiazgd/email-verification-system.git
$ cd email-verification-system/
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install --upgrade pip
$ pip install -r requirements.txt
```
Create .env file
```FLASK_APP=app
FLASK_ENV=development
EMAIL_USER='email_gmail'
EMAIL_PASSWORD='password_gmail'
EMAIL_RECIPIENT='user_email'
```
```
flask run
```
