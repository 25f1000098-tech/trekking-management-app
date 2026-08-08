from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from functools import wraps
from flask import abort
from app import db
from app.models import Trek, Booking

user_bp = Blueprint('user', __name__, url_prefix='/user')

def trekker_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'trekker':
            abort(403)
        return f(*args, **kwargs)
    return decorated


@user_bp.route('/dashboard')
@login_required
@trekker_required
def dashboard():
    query = request.args.get('q', '').strip()
    difficulty = request.args.get('difficulty', '')

    treks_query = Trek.query.filter_by(status='Open')

    if query:
        treks_query = treks_query.filter(Trek.location.ilike(f'%{query}%'))
    if difficulty:
        treks_query = treks_query.filter_by(difficulty=difficulty)

    treks = treks_query.all()

    my_booking_trek_ids = {b.trek_id for b in Booking.query.filter_by(user_id=current_user.id, booking_status='Booked').all()}

    return render_template('user/dashboard.html', treks=treks, query=query, difficulty=difficulty, my_booking_trek_ids=my_booking_trek_ids)

@user_bp.route('/treks/<int:trek_id>/book', methods=['POST'])
@login_required
@trekker_required
def book_trek(trek_id):
    trek = Trek.query.get_or_404(trek_id)

    if trek.status != 'Open':
        flash('This trek is not open for booking.')
        return redirect(url_for('user.dashboard'))

    if trek.available_slots <= 0:
        flash('This trek is full.')
        return redirect(url_for('user.dashboard'))

    existing = Booking.query.filter_by(user_id=current_user.id, trek_id=trek.id, booking_status='Booked').first()
    if existing:
        flash('You have already booked this trek.')
        return redirect(url_for('user.dashboard'))

    new_booking = Booking(user_id=current_user.id, trek_id=trek.id, booking_status='Booked', payment_status='Pending')
    trek.available_slots -= 1

    db.session.add(new_booking)
    db.session.commit()
    flash('Trek booked successfully!')
    return redirect(url_for('user.dashboard'))

@user_bp.route('/my-bookings')
@login_required
@trekker_required
def my_bookings():
    bookings = Booking.query.filter_by(user_id=current_user.id).all()
    return render_template('user/my_bookings.html', bookings=bookings)