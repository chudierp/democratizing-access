# import os
from flask_wtf import FlaskForm, Form
from flask import Flask, redirect, render_template, url_for
from flask_bootstrap import Bootstrap
from wtforms import StringField, PasswordField, BooleanField 
from wtforms.validators import InputRequired, Email, Length


app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = 'Thisissupposetobesecret'


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
        return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'
    
    return render_template('register.html', form=form)        

     

if __name__ == "__main__":
    print(app.secret_key)
    app.run(debug=True)