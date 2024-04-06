from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSONB

db = SQLAlchemy()

class JobApplication(db.Model):
    __tablename__ = 'job_applications'
    id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(255), nullable=False)
    company_name = db.Column(db.String(255), nullable=True)
    location = db.Column(db.String(255), nullable=True)
    work_format = db.Column(db.String(50), nullable=True)
    remote_work_availability = db.Column(db.String(50), nullable=True)
    application_deadline = db.Column(db.Date, nullable=True)
    application_date = db.Column(db.Date, nullable=False)
    salary_range = db.Column(db.String(255), nullable=True)
    required_skills = db.Column(db.ARRAY(db.String), nullable=True)
    benefits = db.Column(db.ARRAY(db.String), nullable=True)
    application_status = db.Column(db.String(50), nullable=False)
    application_link = db.Column(db.Text, nullable=True)
    additional_details = db.Column(db.JSONB, nullable=True)
