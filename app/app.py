from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from data import Articles
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship 
from sqlalchemy import create_engine
from sqlalchemy.sql import func 
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt


app = Flask(__name__)
#Config MySQL
mysql = create_engine('mysql://arasdean:test@localhost/myflaskapp'); 
Base = declarative_base() 

class User(Base): 
    __tablename__ = 'user' 
    id = Column(Integer, primary_key=True, autoincrement=True) 
    name = Column(String(100), nullable=False) 
    email = Column(String(100), nullable=False) 
    username = Column(String(30)) 
    password = Column(String(100)); 
    registered_date = (DateTime(timezone=True), func.now())
    


Articles = Articles()

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/articles')
def articles():
    return render_template('articles.html', articles= Articles)

@app.route('/article/<string:id>')
def article(id):
    return render_template('article.html', id=id)

class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=6, max=20)])
    username = StringField('Username', [validators.Length(min=6, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
    validators.DataRequired(),
    validators.EqualTo('confirm', message='Passwords need to match')])
    confirm = PasswordField('Confirm Pass')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form= RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))
        print('sent') 
        #CREATE CURSOR

        cur = mysql.connection.cursor()

        cur.execute("insert into users(name, email, username, password) valyes (%s, %s, %s, %s)", (name, email, username, password))

        # Commit to DB
        mysql.connection.commit()

        #close connection
        cur.close()

        flash('Registered!')

        redirect(url_for('index'));

        return render_template('register.html', form=form)
    return render_template('register.html', form=form)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
