from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    existing_admin = User.query.filter_by(role='admin').first()
    if existing_admin:
        print("Admin already exists:", existing_admin.username)
    else:
        admin = User(
            username='admin',
            email='admin@trekapp.com',
            password_hash=generate_password_hash('admin123'),
            role='admin',
            is_approved=True,
            is_active=True
        )
        db.session.add(admin)
        db.session.commit()
        print("Admin user created successfully.")