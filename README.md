# Trekking Management Application

A role-based Flask web application for managing treks, trek staff, and trekker bookings — built as a MAD-1 App Dev course project.

## About

The application supports three roles — **Admin**, **Trek Staff**, and **Trekker** — each with a dedicated dashboard and permissions enforced at the route level, not just hidden in the UI. Admins manage treks, staff, and users; Trek Staff manage only the treks assigned to them; Trekkers browse open treks and book them, with server-side checks preventing overbooking and duplicate bookings.

## Tech Stack

- **Backend:** Flask (Python)
- **ORM / Database:** Flask-SQLAlchemy with SQLite
- **Authentication:** Flask-Login, Werkzeug password hashing
- **Templating:** Jinja2, shared base layout, minimal custom CSS
- **Version Control:** Git & GitHub

## Features

### Admin
- Dashboard with live counts of treks, trekkers, staff, and bookings
- Create, edit, and manage treks (name, difficulty, duration, location, slots, status)
- Approve, deactivate, and reactivate Trek Staff accounts
- Deactivate/reactivate Trekker accounts
- Search treks, staff, and trekkers by name or ID
- View all bookings and manually confirm payment status

### Trek Staff
- Dashboard showing only treks assigned to them, with live registered-trekker counts
- Update trek available slots and status (Approved / Open / Closed / Completed)
- View and manage registered trekkers for assigned treks
- Mark bookings as Completed
- Update own staff profile (bio, experience)
- Route-level ownership checks — cannot access or manage treks not assigned to them

### Trekker
- Browse Open treks, with search by location and filter by difficulty
- Book a trek, with server-side checks for full/closed treks and duplicate bookings
- View personal booking history
- Cancel an active booking (automatically frees up the slot)

## Project Structure

```
trekking-management-app/
├── app/
│   ├── __init__.py        # App factory, DB & login manager setup
│   ├── config.py           # App configuration
│   ├── models.py           # User, StaffProfile, Trek, Booking models
│   ├── routes/
│   │   ├── auth.py         # Registration, login, logout, role redirect
│   │   ├── admin.py        # Admin dashboard and management routes
│   │   ├── staff.py        # Trek Staff dashboard and management routes
│   │   └── user.py         # Trekker dashboard and booking routes
│   └── templates/          # Jinja2 templates, organized by role
├── create_admin.py         # One-time script to pre-create the Admin account
├── run.py                  # Application entry point
└── requirements.txt
```

## Setup & Running Locally

1. Clone the repository and create a virtual environment:
   ```bash
   git clone https://github.com/25f1000098-tech/trekking-management-app.git
   cd trekking-management-app
   python -m venv venv
   venv\Scripts\activate      # Windows
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create the pre-defined Admin account (run once):
   ```bash
   python create_admin.py
   ```

4. Run the application:
   ```bash
   python run.py
   ```

5. Visit `http://127.0.0.1:5000/register` to create a Trekker or Trek Staff account, or log in as Admin using the credentials created in step 3.

## Roles & Access Notes

- **Trekkers** are approved automatically on registration.
- **Trek Staff** must register and then be approved by an Admin before they can log in.
- **Admin** cannot be registered through the app — it is pre-created via `create_admin.py`.

## Milestone Progress

| # | Milestone | Status |
|---|---|---|
| 0 | GitHub Repository Setup | ✅ Complete |
| 1 | Database Models & Schema | ✅ Complete |
| 2 | Authentication & Role-Based Access | ✅ Complete |
| 3 | Admin Dashboard & Management | ✅ Complete |
| 4 | Trek Staff Dashboard & Trek Management | ✅ Complete |
| 5 | User Dashboard & Trek Booking System | ✅ Complete |
| 6 | Booking History & Status Tracking | ✅ Complete |

Optional enhancement milestones (API integration, charts, extended validation, Bootstrap styling, additional Flask-Login hardening) are not yet implemented.

## Issues Log

- **Git push "repository not found"** — caused by stale cached GitHub credentials in Windows Credential Manager; resolved by clearing the saved credential and re-authenticating.
- **`venv/` accidentally staged in git** — happened before `.gitignore` was in place; resolved with `git reset` and a properly ordered `.gitignore`.
- **Divergent local/remote histories** — GitHub's auto-created README conflicted with the local initial commit; resolved with `git pull --allow-unrelated-histories`.
- **Duplicate Flask route definitions** (`list_staff`, `list_treks`) — caused app startup errors; resolved by removing the duplicated function blocks.

## AI Usage Declaration

AI assistance (Claude) was used during development for guidance on Flask/SQLAlchemy/Flask-Login concepts, code structure and Git errors. All code was personally written, run, tested, and debugged locally. See the project report for the full declaration and estimated AI involvement percentage.
