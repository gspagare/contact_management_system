# Contact Management System (Flask Project)

A simple and secure Contact Management System built using Flask.  
This project allows users to submit their contact details via a form, and the admin can view the submitted data from a protected dashboard.

---

## Features

- User Contact Form (Name, Email, Phone, Message)
- Data stored in SQLite database
- Admin Login Authentication
- Admin Dashboard to view submitted contacts
- Flash Messages for user feedback
- Clean & Responsive UI
- Secure with environment variables
- Proper folder structure for scalability

---

## Tech Stack

- Python 3.x
- Flask
- Flask-SQLAlchemy
- Flask-Login
- Flask-WTF
- SQLite (Database)
- HTML, CSS, Bootstrap (Frontend)

---

## Installation Guide

### 1. Clone the Repository

        git clone https://github.com/your-username/your-repo-name.git
        cd your-repo-name

### 2. Create Virtual Environment

        python -m venv venv

    ### Windows:
        venv\Scripts\activate

    ### Linux/Mac:
        source venv/bin/activate

### 3. Install Requirements

        pip install -r requirements.txt
        
### 4. Setup Environment Variables

Create a .env file in the root directory:
        FLASK_APP=run.py
        FLASK_ENV=development
        SECRET_KEY=your_secret_key_here

### 5. Run the App

        python app.py

App will be running at:
http://127.0.0.1:5000/

Admin Login Details (Default)
You need to create your admin user in the database manually.

Example:

        from app import db, AdminUser
        admin = AdminUser(username='admin', password=hashed_password)
        db.session.add(admin)
        db.session.commit()

