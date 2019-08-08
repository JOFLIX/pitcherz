from flask import render_template,redirect,url_for,request,flash
from . import auth
from flask_login import login_user,logout_user,login_required
from ..models import User
from .forms import RegistrationForm, LoginForm
from .. import db

# registration route
@auth.route('templates/auth/reqister',methods=['GET','POST'])
def register():
    '''
    function that registaers the users
    '''
    form =RegistrationForm()
    if form.validate_on_submit():
        user =User(email=form.email.data,username=form.username.data,password=form.password.data)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('auth.login'))
    title="Registration"
    return render_template('auth/register.html',registration_form=form,title=title)

# Login function
@auth.route('/login',methods=['GET','POST'])
def login():
    '''
    Function that checks if the form is validated
    '''
    login_form=LoginForm()
    if login_form.validate_on_submit():
        user=User.query.filter_by(email=login_form.email.data).first()
        if user is not None and user.verify_password(login_form.password.data):
            login_user(user,login_form.remember.data)
            return redirect(request.args.get('next')or url_for('main.index'))

        flash('invalid username or password')

    title ="One Minute Pitch|Login"
    return render_template('auth/login.html',login_form=login_form,title=title)

#logout function
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))# redirects user to the main page of the app after successful logout


@auth.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('auth.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)
