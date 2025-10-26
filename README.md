# SnipBox -

SnipBox is a Django REST API for managing code snippets with JWT authentication. Users can create, read, update, and delete their snippets, organize them with tags, and get overviews of their snippet collections.

## Prerequisites

- Python 3.11+
- pip (Python package manager)
- Docker and Docker Compose (for Docker setup)

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd SnipBox
   ```

2. **Create environment file**
   Create a `.env` file in the project root:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   ACCESS_TOKEN_LIFETIME=5
   REFRESH_TOKEN_LIFETIME=1440
   ```

### Option 1: Without Docker

3. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run migrations and Create superuser (first time only)**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

### Option 2: Docker Setup

3. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

4. **Run migrations and Create superuser (first time only)**
   ```bash
   docker-compose exec web python manage.py migrate
   docker-compose exec web python manage.py createsuperuser
   ```

Now The API will be available at `http://localhost:8000`
