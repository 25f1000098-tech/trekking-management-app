from flask import Blueprint, render_template, redirect, url_for, flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User, StaffProfile

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')  # 'trekker' or 'staff'

        existing_user = User.query.filter(
            (User.username == username) | (User.email == email)
        ).first()
        if existing_user:
            flash('Username or email already taken.')
            return redirect(url_for('auth.register'))

        new_user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
            role=role,
            is_approved=(role == 'trekker'),  # trekkers auto-approved, staff need admin approval
            is_active=True
        )
        db.session.add(new_user)
        db.session.commit()

        if role == 'staff':
            profile = StaffProfile(user_id=new_user.id)
            db.session.add(profile)
            db.session.commit()
            flash('Registration successful. Await admin approval before logging in.')
        else:
            flash('Registration successful. You can now log in.')

        return redirect(url_for('auth.login'))

    return render_template('register.html')
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password_hash, password):
            flash('Invalid username or password.')
            return redirect(url_for('auth.login'))

        if not user.is_active:
            flash('This account has been deactivated.')
            return redirect(url_for('auth.login'))

        if user.role == 'staff' and not user.is_approved:
            flash('Your staff account is awaiting admin approval.')
            return redirect(url_for('auth.login'))

        login_user(user)
        return redirect(url_for('auth.dashboard_redirect'))

    return render_template('login.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('auth.login'))


@auth.route('/dashboard')
@login_required
def dashboard_redirect():
    if current_user.role == 'admin':
        return f"Welcome Admin {current_user.username} (dashboard not built yet)"
    elif current_user.role == 'staff':
        return f"Welcome Staff {current_user.username} (dashboard not built yet)"
    else:
        return f"Welcome Trekker {current_user.username} (dashboard not built yet)"