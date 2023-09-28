from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE, bcrypt
from flask import flash, session
import re 
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Admin:

    # CONSTRUCTOR
    def __init__(self, data):
        self.id = data["id"]
        self.user_name = data["user_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    # SQL METHODS

    # CREATE
    @classmethod
    def create(cls, data):
        query = "INSERT INTO admins (user_name, email, password) VALUES ( %(user_name)s, %(email)s, %(password)s );"
        admin_id = connectToMySQL(DATABASE).query_db(query, data)
        return admin_id
    
    # READ ONE
    @classmethod 
    def read_one(cls, data):
        query = "SELECT * FROM admins WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)

        if not result:
            return False
        
        return cls( result[0] )
    
    # READ ONE BY EMAIL
    @classmethod
    def read_one_by_email(cls, data):
        query = "SELECT * FROM admins WHERE email = %(email)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)

        if not result:
            return False
        
        return cls( result[0] )
    
    # UPDATE
    @classmethod
    def update(cls, data):
        query = "UPDATE admins SET user_name = %(user_name)s, email = %(email)s, password = %(password)s WHERE id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        return results
    
    # DELETE
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM admins WHERE id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        return results

    # VALIDATE REGISTRATION 
    @staticmethod
    def validate_registration(data):
        is_valid = True

        if len(data["user_name"]) < 2:
            is_valid = False
            flash("Username must be at least 2 characters.", "err_user_name")
        elif len(data["user_name"]) > 255:
            is_valid = False
            flash("Username must be less than 255 characters.", "err_user_name")
        elif data["user_name"].isspace():
            is_valid = False
            flash("Username cannot be blank.", "err_user_name")
        
        if len(data["email"]) < 2:
            is_valid = False
            flash("Email be at least 2 characters.", "err_email")
        elif len(data["email"]) > 255:
            is_valid = False
            flash("Email must be less than 255 characters.", "err_email")
        elif not EMAIL_REGEX.match(data["email"]):
            is_valid = False
            flash("Invalid email address.", "err_email")
        elif data["email"].isspace():
            is_valid = False
            flash("Email cannot be blank.", "err_email")
        else: 
            potential_user = Admin.read_one_by_email(data)
            if potential_user:
                is_valid = False
                flash("Email already exists!", "err_email")

        if len(data["password"]) < 2:
            is_valid = False
            flash("Password must be at least 2 characters.", "err_password")
        elif len(data["password"]) > 45:
            is_valid = False
            flash("Password must be less than 45 characters.", "err_password")
        elif not data["password"]:
            is_valid = False
            flash("Password cannot be blank.", "err_password")

        if not data["confirm_password"] == data["password"]:
            is_valid = False
            flash("Passwords do not match", "err_confirm_password")
        
        return is_valid

    # VALIDATE LOGIN 
    @staticmethod
    def validate_login(data):
        is_valid = True

        if not data["email"]:
            is_valid = False
            flash("Email required.", "err_email_login")
        elif not EMAIL_REGEX.match(data["email"]):
            is_valid = False
            flash("Invalid email address.", "err_email_login")

        if not data["password"]:
            is_valid = False
            flash("Password required.", "err_password_login")
        
        if is_valid:
            potential_user = Admin.read_one_by_email(data)
            if not potential_user:
                is_valid = False
                flash("Incorrect email or password.", "err_email_login")
            else:
                if not bcrypt.check_password_hash(potential_user.password, data["password"]):
                    is_valid = False
                    flash("Incorrect email or password.", "err_password_login")
                else:
                    session["admin_id"] = potential_user.id
        
        return is_valid
    
    # UPDATE
    @staticmethod
    def validate_update(data):
        is_valid = True

        if len(data["user_name"]) < 2:
            is_valid = False
            flash("Username must be at least 2 characters.", "err_user_name")
        elif len(data["first_name"]) > 255:
            is_valid = False
            flash("Username must be less than 255 characters.", "err_user_name")
        elif not data["first_name"]:
            is_valid = False
            flash("Username cannot be blank.", "err_user_name")
        
        if len(data["email"]) > 255:
            is_valid = False
            flash("Email must be less than 255 characters.", "err_email")
        if not EMAIL_REGEX.match(data["email"]):
            is_valid = False
            flash("Invalid email address.", "err_email")
        elif not data["email"]:
            is_valid = False
            flash("Email cannot be blank.", "err_email")
        else:
            potential_user = Admin.read_one_by_email(data)
            if potential_user and potential_user == data["curr_admin_email"]:
                is_valid = False
                flash("Email already exists!", "err_email")
        return is_valid 