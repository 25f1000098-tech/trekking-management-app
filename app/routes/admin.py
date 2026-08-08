from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import User, Trek, Booking, StaffProfile
from app.routes.auth import admin_required

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    total_treks = Trek.query.count()
    total_users = User.query.filter_by(role='trekker').count()
    total_staff = User.query.filter_by(role='staff').count()
    total_bookings = Booking.query.count()

    return render_template(
        'admin/dashboard.html',
        total_treks=total_treks,
        total_users=total_users,
        total_staff=total_staff,
        total_bookings=total_bookings
    )
@admin_bp.route('/treks/new', methods=['GET', 'POST'])
@login_required
@admin_required
def create_trek():
    if request.method == 'POST':
        name = request.form.get('name')
        difficulty = request.form.get('difficulty')
        duration_days = request.form.get('duration_days')
        location = request.form.get('location')
        available_slots = request.form.get('available_slots')

        new_trek = Trek(
            name=name,
            difficulty=difficulty,
            duration_days=int(duration_days),
            location=location,
            available_slots=int(available_slots),
            status='Pending'
        )
        db.session.add(new_trek)
        db.session.commit()
        flash('Trek created successfully.')
        return redirect(url_for('admin.dashboard'))

    return render_template('admin/create_trek.html')

@admin_bp.route('/treks')
@login_required
@admin_required
def list_treks():
    query = request.args.get('q', '').strip()
    treks_query = Trek.query

    if query:
        if query.isdigit():
            treks_query = treks_query.filter(Trek.id == int(query))
        else:
            treks_query = treks_query.filter(Trek.name.ilike(f'%{query}%'))

    treks = treks_query.all()
    return render_template('admin/list_treks.html', treks=treks, query=query)

@admin_bp.route('/treks/<int:trek_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_trek(trek_id):
    trek = Trek.query.get_or_404(trek_id)
    all_staff = StaffProfile.query.join(User).filter(User.is_approved == True).all()

    if request.method == 'POST':
        trek.name = request.form.get('name')
        trek.difficulty = request.form.get('difficulty')
        trek.duration_days = int(request.form.get('duration_days'))
        trek.location = request.form.get('location')
        trek.available_slots = int(request.form.get('available_slots'))
        trek.status = request.form.get('status')

        staff_id = request.form.get('staff_id')
        trek.staff_id = int(staff_id) if staff_id else None

        db.session.commit()
        flash('Trek updated successfully.')
        return redirect(url_for('admin.list_treks'))

    return render_template('admin/edit_trek.html', trek=trek, all_staff=all_staff)


@admin_bp.route('/staff/<int:user_id>/approve', methods=['POST'])
@login_required
@admin_required
def approve_staff(user_id):
    staff = User.query.get_or_404(user_id)
    staff.is_approved = True
    db.session.commit()
    flash(f'{staff.username} approved.')
    return redirect(url_for('admin.list_staff'))


@admin_bp.route('/staff/<int:user_id>/deactivate', methods=['POST'])
@login_required
@admin_required
def deactivate_staff(user_id):
    staff = User.query.get_or_404(user_id)
    staff.is_active = False
    db.session.commit()
    flash(f'{staff.username} deactivated.')
    return redirect(url_for('admin.list_staff'))


@admin_bp.route('/staff/<int:user_id>/reactivate', methods=['POST'])
@login_required
@admin_required
def reactivate_staff(user_id):
    staff = User.query.get_or_404(user_id)
    staff.is_active = True
    db.session.commit()
    flash(f'{staff.username} reactivated.')
    return redirect(url_for('admin.list_staff'))

@admin_bp.route('/users')
@login_required
@admin_required
def list_users():
    query = request.args.get('q', '').strip()
    users_query = User.query.filter_by(role='trekker')

    if query:
        if query.isdigit():
            users_query = users_query.filter(User.id == int(query))
        else:
            users_query = users_query.filter(User.username.ilike(f'%{query}%'))

    users = users_query.all()
    return render_template('admin/list_users.html', users=users, query=query)

@admin_bp.route('/staff')
@login_required
@admin_required
def list_staff():
    query = request.args.get('q', '').strip()
    staff_query = User.query.filter_by(role='staff')

    if query:
        if query.isdigit():
            staff_query = staff_query.filter(User.id == int(query))
        else:
            staff_query = staff_query.filter(User.username.ilike(f'%{query}%'))

    staff_users = staff_query.all()
    return render_template('admin/list_staff.html', staff_users=staff_users, query=query)


@admin_bp.route('/users/<int:user_id>/deactivate', methods=['POST'])
@login_required
@admin_required
def deactivate_user(user_id):
    user = User.query.get_or_404(user_id)
    user.is_active = False
    db.session.commit()
    flash(f'{user.username} deactivated.')
    return redirect(url_for('admin.list_users'))


@admin_bp.route('/users/<int:user_id>/reactivate', methods=['POST'])
@login_required
@admin_required
def reactivate_user(user_id):
    user = User.query.get_or_404(user_id)
    user.is_active = True
    db.session.commit()
    flash(f'{user.username} reactivated.')
    return redirect(url_for('admin.list_users'))

@admin_bp.route('/bookings')
@login_required
@admin_required
def list_bookings():
    bookings = Booking.query.all()
    return render_template('admin/list_bookings.html', bookings=bookings)

@admin_bp.route('/bookings/<int:booking_id>/mark-paid', methods=['POST'])
@login_required
@admin_required
def mark_paid(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    booking.payment_status = 'Paid'
    db.session.commit()
    flash('Booking marked as paid.')
    return redirect(url_for('admin.list_bookings'))