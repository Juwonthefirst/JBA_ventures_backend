# JBA Ventures Backend

A Django REST Framework backend for a real estate management system that handles property listings, authentication, and media management.

## Table of Contents

- [Features](#features)
- [Technology Stack](#technology-stack)
- [Scripts](#scripts)
- [Setup](#setup)
- [Authentication](#authentication)
- [API Endpoints](#api-endpoints)
- [Models](#models)
- [File Structure](#file-structure)

## Features

- Property listing management with multiple media uploads
- JWT-based authentication with secure refresh token handling
- Advanced property filtering and search capabilities
- Role-based access control (Admin/Read-only)
- Media file organization by location hierarchy
- UV for package management and scripting

## Technology Stack

- UV
- Django
- Django REST Framework
- PostgreSQL (with ArrayField support)
- Simple JWT for authentication
- Django Filter for advanced querying

## Scripts

This project features a scripts.py file containing commands to automate development process by calling `uv run scripts.py <command>`

### Commands

- dev

  ```python
   subprocess.run(["pg_ctl", "-D", postgres_file_location, "start"])
    subprocess.run(["uv", "run", "manage.py", "runserver", "0.0.0.0:8000"])

  ```

- prod

  ```python
    subprocess.run(["python", "createsuperuser.py"])
    subprocess.run(["python", "manage.py", "makemigrations"])
    subprocess.run(["python", "manage.py", "migrate"])
    subprocess.run(["python", "manage.py", "collectstatic"])
    subprocess.run(["gunicorn", "real_estate_api.wsgi:application"])

  ```

- migrate

  ```python
    subprocess.run(["uv", "run", "manage.py", "makemigrations"])
    subprocess.run(["uv", "run", "manage.py", "migrate"])
  ```

- startdb
  ```python
    subprocess.run(["pg_ctl", "-D", postgres_file_location, "start"])
  ```
- stopdb
  ```python
    subprocess.run(["pg_ctl", "-D", postgres_file_location, "stop"])
  ```

Note: This project requires your postgres server to be in Program Files, if it doesn't exist there go to scripts.py file and point the `postgres_file_location` to it's location on your computer

## Setup

1. Clone the repository:

```bash
git clone https://github.com/Juwonthefirst/JBA_ventures_backend.git
cd JBA_ventures_backend
```

2. Install dependencies:

```bash
# Using uv
pip install uv # if it's not already installed
uv sync
```

3. Set up environment variables (create a .env file):

```env
SECRET_KEY=your_secret_key
DEBUG=True
DBNAME=your_db_name
DBUSER=your_db_user
DBPASSWORD=your_db_password
DBHOST=your_db_host_address
DBPORT=your_db_port(defaults to 5432)
```

4. Run migrations:

```bash
uv run scripts.py migrate
```

5. Create a superuser:

```bash
python manage.py createsuperuser
```

6. Run the development server:

```bash
uv run scripts.py dev
```

## Authentication

The API uses JWT (JSON Web Token) authentication with secure refresh token handling. All refresh tokens are stored as HTTP-only cookies for enhanced security.

### Authentication Endpoints

#### Get CSRF Token

```
GET /api/v1/auth/csrf/
```

Returns a CSRF token required for making POST requests.

#### Login

```
POST /api/v1/auth/login/
```

Request body:

```json
{
  "email": "user@example.com",
  "password": "your_password"
}
```

Returns:

```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..." // JWT access token
}
```

Note: Refresh token is set as HTTP-only cookie

#### Refresh Token

```
POST /api/v1/auth/refresh/
```

Automatically uses the refresh token from cookies to generate a new access token.

#### Logout

```
GET /api/v1/auth/logout/
```

Blacklists the current refresh token and removes the cookie.

## API Endpoints

### Properties

#### List/Create Property

```
GET /api/v1/properties/
POST /api/v1/properties/
```

##### GET Response Format

```json
{
  "count": 10,
  "next": "http://api.example.com/properties/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "main_image": "http://api.example.com/media/lagos/ikeja/example-address/apartment/base_image.jpg",
      "state": "Lagos",
      "lga": "Ikeja",
      "description": "Beautiful 3 bedroom apartment...",
      "type": "Apartment",
      "offer": "Sale",
      "price": 25000000,
      "tags": {
        "bedrooms": "3",
        "bathrooms": "2",
        "parking": "Yes"
      },
      "extra_media": [
        {
          "id": 1,
          "media": "http://api.example.com/media/1/extra_media/living_room.jpg"
        },
        {
          "id": 2,
          "media": "http://api.example.com/media/1/extra_media/kitchen.jpg"
        }
      ]
    }
    // ... more properties
  ]
}
```

##### POST Request Format

```json
{
  "main_image": "[binary file]",
  "address": "123 Example Street",
  "state": "Lagos",
  "lga": "Ikeja",
  "description": "Beautiful 3 bedroom apartment...",
  "benefits": ["24/7 Security", "Constant Power", "Swimming Pool"],
  "type": "Apartment",
  "offer": "Sale",
  "price": 25000000,
  "tags": {
    "bedrooms": "3",
    "bathrooms": "2",
    "parking": "Yes"
  },
  "extra_media": ["[binary file]", "[binary file]"]
}
```

Query Parameters for GET:

- `search`: Search in description and benefits
- `state`: Filter by state
- `lga`: Filter by Local Government Area
- `type`: Filter by property type
- `offer`: Filter by offer type
- `price_base`: Minimum price
- `price_roof`: Maximum price
- `tag`: Filter by tags (format: "key:value")

#### Retrieve/Update/Delete Property

```
GET /api/v1/properties/<id>/
PUT /api/v1/properties/<id>/
DELETE /api/v1/properties/<id>/
```

##### GET Response Format

```json
{
  "main_image": "http://api.example.com/media/lagos/ikeja/example-address/apartment/base_image.jpg",
  "address": "123 Example Street",
  "state": "Lagos",
  "lga": "Ikeja",
  "description": "Beautiful 3 bedroom apartment...",
  "benefits": ["24/7 Security", "Constant Power", "Swimming Pool"],
  "type": "Apartment",
  "offer": "Sale",
  "price": 25000000,
  "tags": {
    "bedrooms": "3",
    "bathrooms": "2",
    "parking": "Yes"
  },
  "extra_media": [
    {
      "id": 1,
      "media": "http://api.example.com/media/1/extra_media/living_room.jpg"
    },
    {
      "id": 2,
      "media": "http://api.example.com/media/1/extra_media/kitchen.jpg"
    }
  ]
}
```

##### PUT Request Format

```json
{
  "main_image": "[binary file]", // Optional
  "address": "123 Example Street",
  "state": "Lagos",
  "lga": "Ikeja",
  "description": "Beautiful 3 bedroom apartment...",
  "benefits": ["24/7 Security", "Constant Power", "Swimming Pool"],
  "type": "Apartment",
  "offer": "Sale",
  "price": 25000000,
  "tags": {
    "bedrooms": "3",
    "bathrooms": "2",
    "parking": "Yes"
  },
  "extra_media_upload": ["[binary file]", "[binary file]"] // Optional, adds new media
}
```

- GET: Retrieve a specific property
- PUT: Update a property (Admin only)
- DELETE: Delete a property (Admin only)

## Models

### Property Model

```python
class Property:
    main_image: ImageField
    address: CharField(max_length=200)
    state: CharField(max_length=20)
    lga: CharField(max_length=50)
    description: TextField
    benefits: ArrayField(CharField)
    type: CharField(max_length=50)
    offer: CharField(max_length=50)
    price: BigIntegerField
    tags: JSONField
```

### PropertyMedia Model

```python
class PropertyMedia:
    property: ForeignKey(Property)
    media: FileField
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License.
