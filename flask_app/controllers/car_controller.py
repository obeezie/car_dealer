import re
from flask import redirect, render_template, request, flash, session
from flask_app import app, DATABASE
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user_model import User
from flask_app.models.car_model import Car

@app.route('/dashboard')
def render_dashboard():
    if not session:
        flash("You are not logged in","error_login")
        return redirect("/")
    data={
        "id": session["user_id"]
    }
    cars = Car.get_all()
    user = User.get_user_by_id(data)
    return render_template("dashboard.html", user = user, cars = cars)

@app.route("/add_car")
def render_add_car():
    return render_template("add_car.html")

@app.route("/add_car",methods=["POST"])
def post_car():
    if not Car.validate_car(request.form):
        return redirect("/add_car")
    else:
        data={
            "price": request.form["price"],
            "model": request.form["model"],
            "description": request.form["description"],
            "make": request.form["make"],
            "year": request.form["year"],
            "user_id": request.form["user_id"],
        }
        Car.save_car(data)
    return redirect("/dashboard")

@app.route("/delete_car/<int:id>")
def delete_car(id):
    data = {
        "id": id
    }
    Car.delete_car(data)
    return redirect("/dashboard")

@app.route("/view_car/<int:id>")
def view_car(id):
    data ={
        "id": id
    }
    car = Car.get_car_by_id(data)
    return render_template("view_car.html", car=car)

@app.route("/purchase_car/<int:id>")
def purchase_car(id):
    data ={
        "user_id": session["user_id"],
        "car_id": id
    }
    
    Car.purchase_car(data)
    return redirect("/dashboard")

@app.route("/edit_car_form/<int:id>")
def render_edit_car(id):
    data ={
        "id": id
    }
    car = Car.get_car_by_id(data)
    return render_template("edit_car.html", car = car)

@app.route("/edit_car/<int:id>", methods =["POST"])
def submit_user_edit(id):
    if not Car.validate_car(request.form):
        redirect_page = "/edit_car_form/"
        redirect_page += str(id)
        return redirect(redirect_page)
    else:
        data= {
            "id": id,
            "price": request.form["price"],
            "model": request.form["model"],
            "description": request.form["description"],
            "make": request.form["make"],
            "year": request.form["year"],
            "user_id": request.form["user_id"],
        }
        Car.update_car(data)

    return redirect("/dashboard")




