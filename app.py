from flask import Flask, render_template, request, redirect, url_for, flash, make_response
from flask_login import current_user, login_required, login_user, logout_user
from config import Config
from extensions import db, login_manager
from models import Contact, Admin
from forms import AuditionForm, AdminForm, AdminLoginForm
import csv
from io import StringIO
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime
from dotenv import load_dotenv

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'admin_login'
    
    @login_manager.user_loader
    def load_user(user_id):
        return Admin.query.get(int(user_id))
    
    return app

app = create_app()
load_dotenv()

@app.route('/')
def root():
    return redirect(url_for('home'))

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if current_user.is_authenticated:
        flash('Admins cannot submit forms', 'warning')
        return redirect(url_for('admin_dashboard'))
    
    form = AuditionForm()
    if form.validate_on_submit():
        try:
            age = int(form.age.data)
            if age < 18:
                flash('You must be older than 18 to apply', 'danger')
                return redirect(url_for('contact'))
            
            new_contact = Contact(
                name=form.name.data,
                email=form.email.data,
                phone=form.phone.data,
                audition_type=form.audition_type.data,
                age=age
            )
            db.session.add(new_contact)
            db.session.commit()
            flash('Your application has been submitted successfully!', 'success')
            return redirect(url_for('contact'))
        except ValueError:
            flash('Invalid age format', 'danger')
    return render_template('contact.html', form=form)

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    form = AdminLoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(username=form.username.data).first()
        if admin and check_password_hash(admin.password_hash, form.password.data):
            login_user(admin)
            return redirect(url_for('admin_dashboard'))
        flash('Invalid username or password', 'danger')
    return render_template('admin_login.html', form=form)

@app.route('/admin_dashboard')
@login_required
def admin_dashboard():
    contacts = Contact.query.order_by(Contact.created_at.desc()).all()
    return render_template('admin_dashboard.html', contacts=contacts)

@app.route('/delete-entry/<int:id>')
@login_required
def delete_entry(id):
    contact = Contact.query.get_or_404(id)
    db.session.delete(contact)
    db.session.commit()
    flash('Entry deleted successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/export-csv')
@login_required
def export_csv():
    contacts = Contact.query.all()
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Name', 'Email', 'Phone', 'Audition Type', 'Age', 'Date'])
    for contact in contacts:
        writer.writerow([
            contact.id,
            contact.name,
            contact.email,
            contact.phone,
            contact.audition_type,
            contact.age,
            contact.created_at.strftime('%Y-%m-%d %H:%M')
        ])
    output.seek(0)
    response = make_response(output.getvalue())
    response.headers['Content-Disposition'] = 'attachment; filename=contacts_export.csv'
    response.headers['Content-type'] = 'text/csv'
    return response

@app.route('/admin/manage', methods=['GET', 'POST'])
@login_required
def manage_admins():
    admin_form = AdminForm()
    if admin_form.validate_on_submit():
        hashed_password = generate_password_hash(admin_form.password.data)
        new_admin = Admin(
            username=admin_form.username.data,
            password_hash=hashed_password
        )
        db.session.add(new_admin)
        db.session.commit()
        flash('Admin added successfully!', 'success')
        return redirect(url_for('manage_admins'))
    
    admins = Admin.query.all()
    return render_template('manage_admins.html', 
                         admin_form=admin_form, 
                         admins=admins)

@app.route('/admin/delete/<int:id>')
@login_required
def delete_admin(id):
    if current_user.id == id:
        flash('You cannot delete yourself!', 'danger')
    else:
        admin = Admin.query.get_or_404(id)
        db.session.delete(admin)
        db.session.commit()
        flash('Admin deleted successfully!', 'success')
    return redirect(url_for('manage_admins'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('admin_login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Create initial admin if none exists
        if not Admin.query.first() and os.getenv('ADMIN_USERNAME'):
            admin = Admin(
                username=os.getenv('ADMIN_USERNAME'),
                password_hash=generate_password_hash(os.getenv('ADMIN_PASSWORD', 'admin123'))
            )
            db.session.add(admin)
            db.session.commit()
    app.run(debug=True)