from datetime import datetime
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'admin' / 'staff' / 'trekker'
    is_approved = db.Column(db.Boolean, default=False)   # relevant for staff approval flow
    is_active = db.Column(db.Boolean, default=True)      # for blacklisting/deactivation
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    bookings = db.relationship('Booking', backref='user', lazy=True)
    staff_profile = db.relationship('StaffProfile', backref='user', uselist=False, lazy=True)


class StaffProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)
    bio = db.Column(db.Text, nullable=True)
    experience_years = db.Column(db.Integer, nullable=True)

    treks = db.relationship('Trek', backref='assigned_staff', lazy=True)


class Trek(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)  # Easy / Moderate / Hard
    duration_days = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(120), nullable=False)
    available_slots = db.Column(db.Integer, nullable=False)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff_profile.id'), nullable=True)
    status = db.Column(db.String(20), default='Pending')  # Pending/Approved/Open/Closed/Completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    bookings = db.relationship('Booking', backref='trek', lazy=True)


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    trek_id = db.Column(db.Integer, db.ForeignKey('trek.id'), nullable=False)
    booking_status = db.Column(db.String(20), default='Booked')  # Booked/Cancelled/Completed
    payment_status = db.Column(db.String(20), default='Pending')
    booking_date = db.Column(db.DateTime, default=datetime.utcnow)