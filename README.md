# live-chat


## Install and Run

Create a virtual environment where all the required python packages will be installed

Install all the project Requirements in virtualenv
```bash
pip install -r requirements.txt
```
-Apply migrations and create your superuser (follow the prompts)

# apply migrations and create your database
python manage.py migrate

Run the development server

```bash
# run django development server
python manage.py runserver
```