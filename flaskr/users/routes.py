from flask import render_template, url_for, redirect, Blueprint, flash, request
from flask_login import login_user, current_user, logout_user
from flaskr import db, bcrypt
from flaskr.models import User
from flaskr.users.forms import RegistrationForm, LoginForm


users = Blueprint('users', __name__)


@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('users.login'))

    return render_template(
        'register.html', title='Register', form=form
    )
        

@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccesful. Please check email and password', 'danger')
    return render_template(
        'login.html', title='login', form=form
    )

    
@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))

