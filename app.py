from flask import Flask, render_template, redirect, url_for, flash, request, session
from config import Config
from models import db, Contact
from forms import ContactForm, AdminLoginForm
from flask_login import logout_user, login_required
from flask_login import LoginManager
import os

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)  # Correct way to initialize
login_manager.login_view = 'login'


with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        new_contact = Contact(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            message=form.message.data
        )
        db.session.add(new_contact)
        db.session.commit()
        flash('Your message has been sent!', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html', form=form)

@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    form = AdminLoginForm()
    if form.validate_on_submit():
        if form.username.data == os.getenv('ADMIN_USERNAME') and form.password.data == os.getenv('ADMIN_PASSWORD'):
            session['admin'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid Credentials', 'danger')
    return render_template('admin_login.html', form=form)

@app.route('/admin-dashboard')
def admin_dashboard():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    contacts = Contact.query.all()
    return render_template('admin_dashboard.html', contacts=contacts)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
