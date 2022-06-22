from flask_app.config.mysqlconnection import connectToMySQL

from flask_app import DATABASE
from flask import flash
import re



EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password= data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(DATABASE).query_db(query)
        users = []
        for user in results:
            users.append( cls(user))
        return users

    @classmethod
    def get_user_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)

        if len(result) > 0:
            return cls( result[0] )
        else:
            return None

    @classmethod
    def get_user_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)

        return result[0]

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users "
        query += "(first_name, last_name, email, password, created_at, updated_at) "
        query += "VALUES(%(first_name)s,%(last_name)s, %(email)s, %(password)s, NOW(), NOW() );"
        return connectToMySQL(DATABASE).query_db(query, data)



    @staticmethod
    def validate_user(user):
        is_valid= True
        if len(user['first_name']) < 2:
            flash("First name must be at least 2 characters.", "error_first_name")
            is_valid= False
        if len(user['last_name']) < 2:
            flash("Last name must be at least 2 characters.", "error_last_name")
            is_valid= False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address!", "error_email")
            is_valid = False
        if len(user['password']) < 7:
            flash("Password must be at least 8 characters", "error_password")
            is_valid = False
        if user['password'] != user['password_check']:
            flash("The passwords do not match", "error_mismatch")
            is_valid = False
                
        return is_valid



    @classmethod
    def get_user_purchases(cls, data):
        query= "SELECT purchased_cars.*, cars.make, cars.model, cars.year "
        query += "FROM purchased_cars JOIN cars ON purchased_cars.car_id = cars.id "
        query += "WHERE purchased_cars.user_id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        purchases = []

        for purchase in result:
            purchases.append(
                purchase
            )

        return purchases