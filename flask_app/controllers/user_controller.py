import re
from flask import redirect, render_template, request, flash, session
from flask_app import app
from flask_app.models.user_model import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def register_login():
    return render_template("index.html")

@app.route('/create_user', methods=["POST"])
def create_user():
    
    if not User.validate_user(request.form):
        print("check")
        return redirect('/')
    else:
        if User.get_user_by_email({"email" : request.form['email']}) == None:
            data= {
                "first_name": request.form["first_name"],
                "last_name": request.form["last_name"],
                "email": request.form["email"],
                "password": bcrypt.generate_password_hash(request.form["password"])
            }
            print(data)

            User.save(data)
            print("user added")
            return redirect("/")
        else:
            flash("This email is already in use, please choose another email", "error_email")
            return redirect("/")

@app.route('/login', methods=['POST'])
def login():
    data = {"email" : request.form["email"]}
    user = User.get_user_by_email(data)

    if not user:
        flash("Invalid Email/Password")
        return redirect("/")
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Email/Password")
        return redirect('/')

    if len(request.form["email"]) == 0:
        flash("Invalid Email/Password", "error_credentials")
        return redirect("/")
    if len(request.form["password"]) == 0:
        flash("Invalid Email/Password", "error_credentials")
        return redirect("/")

    session["user_id"] = user.id
    return redirect("/dashboard")



@app.route('/logout')
def logout():
    session.clear()
    return redirect("/")

@app.route('/user_purchases')
def render_purchases():
    if not session:
        flash("You are not logged in", "error_login")
        return redirect("/")

    data= {
        "id": session["user_id"]
    }
    user = User.get_user_by_id(data)
    purchases = User.get_user_purchases(data)
    return render_template("purchases.html", purchases = purchases, user = user)