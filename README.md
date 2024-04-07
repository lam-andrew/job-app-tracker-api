# job-app-tracker-api

The backend API for the job application status tracker, which handles all interactions with the database and external services.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.8 or higher
- pip
- PostgreSQL
- A virtual environment (recommended)

### Installation

1. **Clone the repository**:

```
git clone https://github.com/lam-andrew/job-app-tracker-api.git
cd job-app-status-tracker
```

2. **Set up a Python virtual environment** (optional but recommended):

```
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. **Install required Python packages**:

`pip install -r requirements.txt`

### Setting up PostgreSQL

1. Install PostgreSQL and start the PostgreSQL service on your machine.
2. Create a new PostgreSQL database for the application.
3. Execute the necessary SQL commands to prepare your database (consider providing an SQL script or detailed steps).

### Configuration

Set up the required environment variables:

- `OPENAI_API_KEY`: Your OpenAI API key for integrating with OpenAI services.
- `DATABASE_URL`: Your database connection string, for example, `postgresql://username:password@localhost:5432/job_applications`.

Example of setting environment variables in Unix-based systems:

```
export OPENAI_API_KEY='your_openai_api_key_here'
export DATABASE_URL='your_database_url_here'
```

For Windows, use `set` instead of `export`.

### Running the Application

To start the Flask app locally:

`python app.py`

This command will launch the backend server on `http://localhost:5000` by default.

## API Endpoints

(Document the available API endpoints, including their methods, request bodies, and expected responses.)

## Built With

- [Flask](https://flask.palletsprojects.com/) - The web framework used.
- [SQLAlchemy](https://www.sqlalchemy.org/) - ORM library.
- [PostgreSQL](https://www.postgresql.org/) - The database system.
