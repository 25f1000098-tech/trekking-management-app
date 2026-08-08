from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from functools import wraps
from flask import abort
from app import db
from app.models import Trek, StaffProfile, Booking

staff_bp = Blueprint('staff', __name__, url_prefix='/staff')

def staff_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'staff':
            abort(403)
        return f(*args, **kwargs)
    return decorated


@staff_bp.route('/dashboard')
@login_required
@staff_required
def dashboard():
    profile = StaffProfile.query.filter_by(user_id=current_user.id).first()
    assigned_treks = profile.treks if profile else []

    trek_data = []
    for trek in assigned_treks:
        trekker_count = Booking.query.filter_by(trek_id=trek.id, booking_status='Booked').count()
        trek_data.append({'trek': trek, 'trekker_count': trekker_count})

    return render_template('staff/dashboard.html', trek_data=trek_data)

@staff_bp.route('/treks/<int:trek_id>/manage', methods=['GET', 'POST'])
@login_required
@staff_required
def manage_trek(trek_id):
    trek = Trek.query.get_or_404(trek_id)

    # Ownership check: this staff member must actually be assigned to this trek
    profile = StaffProfile.query.filter_by(user_id=current_user.id).first()
    if not profile or trek.staff_id != profile.id:
        abort(403)

    if request.method == 'POST':
        trek.available_slots = int(request.form.get('available_slots'))
        trek.status = request.form.get('status')
        db.session.commit()
        flash('Trek updated successfully.')
        return redirect(url_for('staff.dashboard'))

    bookings = Booking.query.filter_by(trek_id=trek.id).all()
    return render_template('staff/manage_trek.html', trek=trek, bookings=bookings)

@staff_bp.route('/profile', methods=['GET', 'POST'])
@login_required
@staff_required
def profile():
    staff_profile = StaffProfile.query.filter_by(user_id=current_user.id).first()

    if request.method == 'POST':
        staff_profile.bio = request.form.get('bio')
        experience = request.form.get('experience_years')
        staff_profile.experience_years = int(experience) if experience else None
        db.session.commit()
        flash('Profile updated successfully.')
        return redirect(url_for('staff.dashboard'))

    return render_template('staff/profile.html', profile=staff_profile)

@staff_bp.route('/bookings/<int:booking_id>/complete', methods=['POST'])
@login_required
@staff_required
def complete_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    profile = StaffProfile.query.filter_by(user_id=current_user.id).first()

    if not profile or booking.trek.staff_id != profile.id:
        abort(403)

    if booking.booking_status != 'Booked':
        flash('This booking cannot be marked completed.')
        return redirect(url_for('staff.manage_trek', trek_id=booking.trek_id))

    booking.booking_status = 'Completed'
    db.session.commit()
    flash('Booking marked as completed.')
    return redirect(url_for('staff.manage_trek', trek_id=booking.trek_id))