from datetime import datetime, date
import json
import os
from openai import OpenAI
from flask import Flask, request, jsonify
from flask_cors import CORS
import pytz
from models import User, db, JobApplication
from sqlalchemy import text

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL').replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route("/hello")
def hello():
    return "Hello World"


@app.route('/test-connection', methods=['GET'])
def test_db_connection():
    try:
        # Assuming you have a simple query that tests the DB connection
        some_test_query_result = db.session.execute(text('SELECT 1')).scalar()
        print(f"DB QUERY RESULT: {some_test_query_result}")
        return jsonify({"message": "Database connection successful"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route('/create_user', methods=['POST'])
def create_user():
    data = request.json
    user_id = data.get('googleId')
    name = data.get('name')
    email = data.get('email')
    picture_url = data.get('picture')
    
    existing_user = User.query.get(user_id)
    if existing_user:
        return jsonify({"message": "User already exists"}), 200
    
    new_user = User(id=user_id, name=name, email=email, picture_url=picture_url)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "New user created", "user_id": user_id}), 201


@app.route('/jobs', methods=['GET'])
def get_jobs():
    user_id = request.args.get('userId')  # Get userId from query parameters
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    jobs = JobApplication.query.filter_by(user_id=user_id).all()  # Filter by user_id
    return jsonify([{
        'id': job.id,
        'job_title': job.job_title,
        'company_name': job.company_name,
        'location': job.location,
        'work_format': job.work_format,
        'remote_work_availability': job.remote_work_availability,
        'application_deadline': job.application_deadline.isoformat() if job.application_deadline else None,
        'application_date': job.application_date.isoformat(),
        'salary_range': job.salary_range,
        'required_skills': job.required_skills,
        'benefits': job.benefits,
        'application_status': job.application_status,
        'application_link': job.application_link,
        'additional_details': job.additional_details
    } for job in jobs])

with app.app_context():
    db.create_all()


@app.route("/insert_job", methods=['POST'])
def insert_job():
    data = request.json  # Assuming JSON data is sent in the request body
    job_desc_input = data.get('job_desc_input')
    user_id = data.get('user_id')
    timezone = pytz.timezone('America/New_York')
    current_date = datetime.now(timezone).strftime('%Y-%m-%d')
    print(f"CURRENT DATE: {current_date}")

    api_prompt=f'''
    Given the following job description, extract and structure the essential details into a JSON format including the Job Title, Company Name, Location, Work Format, Remote Work Availability, Application Deadline, and any additional relevant details you can find. 
    If certain information cannot be found within the job description, please identify those fields as null. Do not attempt to assume any unspecified attributes based on the context, but ensure all fields are present in the final JSON. 
    Add an Application Date as the current date to track when the job description was entered and set the Application Status to 'Applied' as a default for the entry.
    Note: The "ApplicationDate" field should be set to the date on which this prompt is being processed. Today: {current_date}.
    If there are any additional details that you find in the job description that are not current an attribute of the json template below, please add them into the nested AdditionalDetails json

    ---

    {job_desc_input}

    ---

    Please structure the information as follows:

    {{
    "JobTitle": "<Job Title or null>",
    "CompanyName": "<Company Name or null>",
    "Location": "<Location or null>",
    "WorkFormat": "<Full-Time/Part-Time/Contract/Internship or null>",
    "RemoteWorkAvailability": "<Onsite/Remote/Hybrid or null>",
    "ApplicationDeadline": "<YYYY-MM-DD or null>",
    "ApplicationDate": "Insert {current_date} in YYYY-MM-DD format",
    "SalaryRange": "<If available or null>",
    "RequiredSkills": ["<Skill 1>", "<Skill 2>", "... or null"],
    "Benefits": ["<Benefit 1>", "<Benefit 2>", "... or null"],
    "ApplicationStatus": "Applied",
    "AdditionalDetails": {{
        "ApplicationLink": "<URL if available or null>"
    }}
    "user_id": {user_id}
    }}
    '''

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": api_prompt,
            }
        ],
        response_format={"type": "json_object"},
        model="gpt-4-1106-preview",
    )

    job_json = json.loads(chat_completion.choices[0].message.content)

    # Handle potentially None dates
    application_deadline_str = job_json.get("ApplicationDeadline")
    application_date_str = job_json.get("ApplicationDate")

    if application_deadline_str:
        application_deadline = datetime.strptime(application_deadline_str, "%Y-%m-%d").date()
    else:
        application_deadline = None  # Or set a default value

    if application_date_str:
        application_date = datetime.strptime(application_date_str, "%Y-%m-%d").date()
    else:
        application_date = date.today()

    # Create a new JobApplication instance
    new_job_application = JobApplication(
        job_title=job_json.get("JobTitle"),
        company_name=job_json.get("CompanyName"),
        location=job_json.get("Location"),
        work_format=job_json.get("WorkFormat"),
        remote_work_availability=job_json.get("RemoteWorkAvailability"),
        application_deadline=application_deadline,
        application_date=application_date,
        salary_range=job_json.get("SalaryRange"),
        required_skills=job_json.get("RequiredSkills"),
        benefits=job_json.get("Benefits"),
        application_status=job_json.get("ApplicationStatus"),
        application_link=job_json.get("ApplicationLink"),
        additional_details=job_json.get("AdditionalDetails"),
        user_id=user_id
    )

    db.session.add(new_job_application)
    db.session.commit()

    return jsonify({"message": "Job application inserted successfully", "job_id": new_job_application.id, "job_json": job_json, "user_id": user_id})

@app.route('/jobs/<int:job_id>/status', methods=['PUT'])
def update_job_status(job_id):
    # Get the new status from the request body
    data = request.json
    new_status = data.get('status')

    if not new_status:
        return jsonify({"error": "Status is required."}), 400

    # Find the job application by ID
    job_application = JobApplication.query.get(job_id)
    if not job_application:
        return jsonify({"error": "Job application not found."}), 404

    # Update the job application's status
    job_application.application_status = new_status
    db.session.commit()

    return jsonify({"message": "Job application status updated successfully.", "job_id": job_id, "new_status": new_status})


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensure this is called within app context to setup db tables
    app.run(debug=True)
