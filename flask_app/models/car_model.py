from sqlite3 import connect
from flask_app.config.mysqlconnection import connectToMySQL

from flask_app import DATABASE
from flask import flash
import re

class Car:
    def __init__(self, data):
        self.id = data["id"]
        self.price = data["price"]
        self.model = data["model"]
        self.make = data["make"]
        self.year = data["year"]
        self.description = data["description"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.user_id = data["user_id"]
        self.sold = data["sold"]


    @classmethod
    def get_all(cls):
        query = "SELECT cars.*, users.first_name, users.last_name FROM cars JOIN users ON cars.user_id = users.id"
        results = connectToMySQL(DATABASE).query_db(query)
        print(results)
        cars = []
        for car in results:
            cars.append( cls(car) )
        return cars

    @classmethod
    def get_car_by_id(cls, data):
        query = "SELECT cars.*, users.first_name, users.last_name "
        query+= "FROM cars JOIN users ON cars.user_id = users.id "
        query+= "WHERE cars.id = %(id)s "
        result = connectToMySQL(DATABASE).query_db(query, data)
        if len(result) > 0:
            return result[0]
        else:
            return None


    @classmethod
    def save_car(cls, data):

        query = "INSERT INTO cars (price, model, make, year, description, created_at, updated_at, user_id) "
        query += "VALUES(%(price)s, %(model)s, %(make)s, %(year)s, %(description)s, NOW(), NOW(), %(user_id)s);"

        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def delete_car(cls, data):
        query = "DELETE FROM cars WHERE id = %(id)s;"
        connectToMySQL(DATABASE).query_db(query, data)

        return

    @classmethod
    def purchase_car(cls, data):
        query ="UPDATE cars SET sold = 1 WHERE id = %(car_id)s;"
        connectToMySQL(DATABASE).query_db(query, data)

        query = "INSERT INTO purchased_cars (user_id, car_id) "
        query +="VALUES (%(user_id)s, %(car_id)s);"

        return connectToMySQL(DATABASE).query_db(query,data)

    @classmethod
    def update_car(cls, data):
        query = "UPDATE cars "
        query += "SET make = %(make)s, model = %(model)s, year = %(year)s, price = %(price)s, description = %(description)s, updated_at = NOW() "
        query += "WHERE id = %(id)s;"
        connectToMySQL(DATABASE).query_db(query, data)

        return

    @staticmethod
    def validate_car(data):
        is_valid = True
        if len(data['price']) == 0:
            flash("You must input something into this field", "error_price")
            is_valid = False
        elif int(data['price']) < 0:
            flash("The price must be greater than 0", "error_invalid_price")
            is_valid = False

        if len(data['year']) == 0:
            flash("You must input something into this field", "error_year")
            is_valid = False
        elif int(data['year']) < 0:
            flash("The year must be greater than 0","error_invalid_year")
            is_valid = False
        
            
        if len(data["model"]) == 0:
            flash("You must input something into this field", "error_model")
            is_valid = False
        if len(data["make"]) == 0:
            flash("You must input something into this field", "error_make")
            is_valid = False
        if len(data["description"]) == 0:
            flash("You must input something into this field", "error_description")
            is_valid = False

        return is_valid

