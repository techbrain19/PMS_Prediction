# PMS Price Prediction application

## Setup

The first thing to do is to clone the repository:

```sh
git clone https://github.com/techbrain19/PMS_Prediction.git
cd /PMS_Prediction
```

Create a virtual environment to install dependencies in and activate it:

```sh
python -m venv env
```
To activate virtual environment in MacOS

```sh
source env/bin/activate
```

To activate virtual environment in window

```sh
env\Scripts\activate
```

install the dependencies:

```sh
pip install -r requirements.txt
```

Make migration to create the model table in database
```sh
python manage.py makemigrations
```

Then your have to migrate it
```sh
python manage.py migrate
```

Run the server with

```sh
python manage.py runserver
```
