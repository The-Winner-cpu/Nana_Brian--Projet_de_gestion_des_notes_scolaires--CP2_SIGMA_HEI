from flask import render_template, request, redirect, url_for
from extensions import db
from models.user import User
from werkzeug.security import generate_password_hash

def register():
    if request.method == 'POST':
        username= request.form.get('username')
        email= request.form.get('email')
        password= request.form.get('password')
        hashed_password= generate_password_hash(password)
        new_user= User(
            username= username,
            email= email,
            password= hashed_password,
            role= 'user'
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')


from flask_login import login_user
from werkzeug.security import check_password_hash

def login():
    if request.method == 'POST':
        email= request.form.get('email')
        password= request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            if user.email == "rivalninana7@gmail.com":
                user.role= 'admin'
                db.session.commit()
            login_user(user)
            return redirect('/dashboard')
        return "Ton email ou ton mot de passe est incorrect man ! "
    return render_template('login.html')