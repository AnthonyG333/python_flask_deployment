from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE, bcrypt
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Option:

    # CONSTRUCTOR
    def __init__(self, data):
        self.id = data["id"]
        self.image = data["image"]
        self.name = data["name"]
        self.category = data["category"]
        self.detail = data["detail"]
        self.price = data["price"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    # SQL METHODS

    # CREATE w/out Image
    @classmethod
    def create(cls, data):
        query = "INSERT INTO options (image, name, category, detail, price) VALUES (%(image)s, %(name)s, %(category)s, %(detail)s, %(price)s );"
        option_id = connectToMySQL(DATABASE).query_db(query, data)
        return option_id
    
    # READ ONE 
    @classmethod
    def read_one(cls, data):
        query = "SELECT * FROM options WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)

        if not result:
            return False
        
        return cls( result[0] )

    # READ ONE BY CATEGORY
    @classmethod 
    def read_all_by_category(cls, data):
        query = "SELECT * FROM options WHERE category = %(category)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)

        if not result:
            return False
        
        all_options = []
        for dict in result:
            all_options.append(cls(dict))
        return all_options
    
    # UPDATE
    @classmethod
    def update(cls, data):
        query = "UPDATE options SET image = %(image)s, name = %(name)s, category = %(category)s, detail = %(detail)s, price = %(price)s WHERE id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        return results
    
    # DELETE
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM options WHERE id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        return results
    
    # VALDIDATE CREATE
    @staticmethod
    def validate_create(data):
        is_valid = True
        
        if not data["name"]:
            is_valid = False
            flash("Name is required.", "err_name")
        
        if not data["category"]:
            is_valid = False
            flash("Category is required.", "err_category")
        
        if not data["detail"]:
            is_valid = False
            flash("Detail is required.", "err_detail")
        
        if not data["price"]:
            is_valid = False
            flash("Price is required.", "err_price")

        return is_valid
    
    # VALIDATE CHECKOUT
    @staticmethod
    def validate_checkout(data):
        is_valid = True

        if not data["email"]:
            is_valid = False
            flash("Email is required.", "err_email_1")
        elif not EMAIL_REGEX.match(data["email"]):
            is_valid = False
            flash("Invalid email address.", "err_email_2")
        if not data["first_name"]:
            is_valid = False
            flash("First name is required.", "err_first_name")
        elif data["first_name"].isspace():
            is_valid = False
            flash("Username cannot be blank.", "err_first_name")
        if not data["last_name"]:
            is_valid = False
            flash("Last Name is required", "err_last_name")
        elif data["last_name"].isspace():
            is_valid = False
            flash("Last name cannot be blank.", "err_last_name")
        if not data["card_number"]:
            is_valid = False
            flash("Card number is required.", "err_card_number")
        elif len(data["card_number"]) < 15  or len(data["card_number"]) > 16:
            is_valid = False
            flash("Card number must be 15 or 16 digits.", "err_card_number")
        elif data["card_number"].isalpha():
            is_valid = False
            flash("Card number can only contain numbers.", "err_card_number")
        if data["expiration_year"] == "2023":
            if data["expiration_month"] == "01":
                is_valid == False
                flash("Invalid expiration date.", "err_invalid_expiration_date")
            if data["expiration_month"] == "02":
                is_valid == False
                flash("Invalid expiration date.", "err_invalid_expiration_date")
            if data["expiration_month"] == "03":
                is_valid == False
                flash("Invalid expiration date.", "err_invalid_expiration_date")
            if data["expiration_month"] == "04":
                is_valid == False
                flash("Invalid expiration date.", "err_invalid_expiration_date")
            if data["expiration_month"] == "05":
                is_valid == False
                flash("Invalid expiration date.", "err_invalid_expiration_date")
            if data["expiration_month"] == "06":
                is_valid == False
                flash("Invalid expiration date.", "err_invalid_expiration_date")
            if data["expiration_month"] == "07":
                is_valid == False
                flash("Invalid expiration date.", "err_invalid_expiration_date")
            if data["expiration_month"] == "08":
                is_valid == False
                flash("Invalid expiration date.", "err_invalid_expiration_date")
            if data["expiration_month"] == "09":
                is_valid == False
                flash("Invalid expiration date.", "err_invalid_expiration_date")
        if len(data["security_code"]) < 3 or len(data["security_code"]) > 4: 
            is_valid = False
            flash("Invalid security code.", "err_security_code")

        return is_valid
