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


---

## Deployment

Instructions on how to deploy the application on a live system, such as Heroku:

### Heroku Setup

1. **Install the Heroku CLI**: Ensure you have the Heroku Command Line Interface (CLI) installed on your system. You can download it from [Heroku's website](https://devcenter.heroku.com/articles/heroku-cli).

2. **Login to Heroku**: Open your terminal and log in to Heroku using the command `heroku login`. This opens your web browser to log in to your Heroku account.

### Create a Heroku App

- Execute `heroku create` to create a new app on Heroku. This command outputs the web URL for your application and a Git URL. Note down the web URL, as you'll need it to access your deployed application.

### Set Up Environment Variables

- Set any necessary environment variables on Heroku using the command `heroku config:set VAR_NAME=value`. For each environment variable required by your application, repeat this command with the appropriate `VAR_NAME` and `value`. For example:

```bash
heroku config:set REACT_APP_API_URL=https://your-api-url.com
```

### Configure Buildpacks

- Depending on your application's stack, you may need to specify one or more buildpacks. Heroku uses buildpacks to determine how to build and run your application.
  - For a **Node.js** application, set the Node.js buildpack:
```bash
heroku buildpacks:set heroku/nodejs
```
  - For applications that require **multiple languages** (e.g., a React frontend and a Python Flask backend), add buildpacks in the order they should be executed:
```bash
heroku buildpacks:add --index 1 heroku/nodejs
heroku buildpacks:add --index 2 heroku/python
```

### Deploy Your Application

- **Deploy your application** by pushing your code to the Heroku remote. If your main branch is named `main`, use:
```bash
git push heroku main
```

Replace main with the name of your branch if using a different branch name.  
- Monitor the deployment process by viewing the logs with:
```bash
heroku logs --tail
```

### Access Your Deployed Application
- Once deployed, access your application through the web URL provided by Heroku. You can also open your app directly from the CLI with:
```bash
heroku open
```

### Additional Considerations
- Database Setup: If your application uses a database, make sure to provision and configure the appropriate add-on in Heroku.

- Custom Domain: Configure a custom domain via the Heroku dashboard or CLI if required.

- Performance and Scaling: Monitor your application's performance. Scale dynos as needed to handle the load efficiently.