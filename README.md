
##Introduction

This API allows you to manage inventory items and suppliers for an online store. It provides endpoints for creating, updating, retrieving inventory items and suppliers, and deleting inventory items with JWT authentication for secure acces

## Installation and Setup
#### Prerequisites
- Python 3.8+
- pip
- Virtualenv (recommended)
#### Clone the Repository
> git clone https://github.com/royalty0013/online-store-inventory.git
> cd online-store-inventory
#### Create a Virtual Environment
> python -m venv venv
> source venv/bin/activate
#### Install Dependencies
> pip install -r requirements.txt

## Running the Application
#### Apply Migrations
> python manage.py migrate
#### Create a Superuser
> python manage.py createsuperuser
#### Start the Development Server
> python manage.py runserver

## API Endpoints
> Access API doc here : http://localhost:8000/api/schema/swagger-ui/

## Testing
#### To run the tests, use the following command:
`pytest`
> Ensure you have the necessary configurations in pytest.ini
>
> [pytest]
> DJANGO_SETTINGS_MODULE = online_store_inventory.settings
> python_files = tests.py test_*.py *_tests.py
> addopts = -v
