# import os
from flask_wtf import FlaskForm, Form
from flask import Flask, redirect, render_template, url_for
from flask_bootstrap import Bootstrap
from wtforms import StringField, PasswordField, BooleanField 
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = 'Thisissupposetobesecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/chudierpelpel/MAKESCHOOL/dasv/⁩database.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))


class LoginForm(FlaskForm):
    username = StringField("username",validators=[InputRequired(), Length(min=4, max=15,)])
    password = PasswordField("password", validators=[InputRequired(), Length(min=6, max=80)])
    # remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

        return '<h1>Invalid username or password</h1>'
        
        # return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'
    
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()


        return '<h1>New user has been created</h1>'
        
   
    return render_template('register.html', form=form)        



if __name__ == "__main__":
    print(app.secret_key)
    app.run(debug=True)
