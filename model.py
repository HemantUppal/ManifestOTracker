from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50))
    phone = db.Column(db.Integer, nullable=False)
    pincode = db.Column(db.Integer)
    aadhar = db.Column(db.Integer, nullable=False)

    # Relationships
    votes = db.relationship('Votes', backref='user', lazy=True)
    complaints = db.relationship('Complaint', backref='user', lazy=True)

class Manifesto(db.Model):
    scheme_id = db.Column(db.Integer, primary_key=True)
    scheme_name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(150))
    scheme_type = db.Column(db.String(50))  # central or state
    start_year = db.Column(db.Integer)
    end_year = db.Column(db.Integer)
    status = db.Column(db.String(50))
    source_link = db.Column(db.String(150))
    tenure=db.Column(db.String(50))

    # Relationships
    votes = db.relationship('Votes', backref='scheme', lazy=True)
    complaints = db.relationship('Complaint', backref='scheme', lazy=True)
    reports = db.relationship('Reports', backref='scheme', lazy=True, uselist=False)

class Votes(db.Model):
    vote_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    scheme_id = db.Column(db.Integer, db.ForeignKey('manifesto.scheme_id'), nullable=False)
    upvote = db.Column(db.Integer, default=0)
    downvote = db.Column(db.Integer, default=0)


class Complaint(db.Model):
    complaint_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    scheme_id = db.Column(db.Integer, db.ForeignKey('manifesto.scheme_id'), nullable=False)
    description = db.Column(db.String(150))
    document_link = db.Column(db.String(150))
    status = db.Column(db.String(150), default="Pending")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Reports(db.Model):
    report_id = db.Column(db.Integer, primary_key=True)
    scheme_id = db.Column(db.Integer, db.ForeignKey('manifesto.scheme_id'), nullable=False, unique=True)
    total_votes = db.Column(db.Integer, default=0)
    total_positive = db.Column(db.Integer, default=0)
    total_negative = db.Column(db.Integer, default=0)
    total_complaints = db.Column(db.Integer, default=0)
