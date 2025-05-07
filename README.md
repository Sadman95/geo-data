
# CodeFusion Country Data Project

A Django application that fetches and stores country data from the REST Countries API.

## Setup Instructions

1. **Create a virtual environment**:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```
   pip install -r requirements.txt
   ```

3. **Configure PostgreSQL**:
   - Create a PostgreSQL database named `country_db`
   - Update the `.env` file with your database credentials if needed

4. **Run migrations**:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a superuser**:
   ```
   python manage.py createsuperuser
   ```

6. **Fetch country data**:
   ```
   python manage.py fetch_countries
   ```

7. **Run the development server**:
   ```
   python manage.py runserver
   ```

8. **Access the admin interface**:
   Open your browser and go to `http://127.0.0.1:8000/admin`

## Data Model

The project includes the following models:
- **Country**: Stores basic country information (name, population, flags, etc.)
- **Currency**: Stores currencies used by each country
- **Language**: Stores languages spoken in each country
- **Border**: Represents border relationships between countries

## Updating Data

To update the country data from the API:
```
python manage.py fetch_countries
```

To clear existing data and fetch fresh data:
```
python manage.py fetch_countries --clear
```
