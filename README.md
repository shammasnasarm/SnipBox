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

## API Collections

### Postman Collections

Ready-to-use Postman collections are available in the `API-collections/` directory:

#### Available Collections:

1. **`Auth.postman_collection.json`** - Authentication endpoints
   - Login (Get Access Token)
   - Refresh Token
   - **Auto-token management**: Automatically saves tokens to environment variables

2. **`Snippet.postman_collection.json`** - Snippet management endpoints
   - List (Overview)
   - Detail (Get specific snippet)
   - Create
   - Update (PUT)
   - Delete

3. **`Tags.postman_collection.json`** - Tag management endpoints
   - Tags List
   - Snippets under tag

4. **`dev.postman_environment.json`** - Development environment variables
   - `baseURL`: Your API base URL
   - `access_token`: JWT access token (auto-populated)
   - `refresh_token`: JWT refresh token (auto-populated)

### How to Import:

1. **Import Collections:**
   - Open Postman
   - Click "Import" button
   - Select "File" tab
   - Import all `.postman_collection.json` files from `API-collections/` directory

2. **Import Environment:**
   - Click "Import" button
   - Select "File" tab
   - Import `dev.postman_environment.json`
   - Set the `baseURL` variable to `http://localhost:8000/api`

### Environment Variables Setup:

The environment file (`dev.postman_environment.json`) includes:
- `baseURL`: Set to your API base URL (e.g., `http://localhost:8000/api`)
- `access_token`: Automatically populated after login and refresh
- `refresh_token`: Automatically populated after login

### Quick Start with Collections:

1. **Set Base URL**: Update `baseURL` in the environment to `http://localhost:8000/api`
2. **Login**: Run the "Login" request from Auth collection with your credentials
3. **Auto-token Management**: Tokens are automatically saved to environment variables
4. **Test Endpoints**: All other requests will use the saved tokens automatically
