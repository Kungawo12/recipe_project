from belt_review_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re 

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 


class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
    
    @classmethod
    def get_all_users(cls):
        query= "SELECT * FROM users"
        results= connectToMySQL('recipe_db').query_db(query)
        users = []
        
        for user in results:
            users.append(cls(user))
        return users
    
    def full_name(self):
        full_name= f" {self.first_name} {self.last_name}"
        return full_name
    
    @classmethod
    def save(cls,data):
        query = """INSERT INTO users(first_name,last_name,email,password)
                    VALUES(%(first_name)s,%(last_name)s,%(email)s,%(password)s);
        """
        return connectToMySQL('recipe_db').query_db(query,data)
    
    @classmethod
    def show_user(cls,data):
        query ="SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL('recipe_db').query_db(query,data)
        return cls(results[0])
    
    
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('recipe_db').query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @staticmethod
    def validate_register(data):
        is_valid = True
        if len(data['first_name']) < 2:
            flash('First name must at least 2 characters',"register")
            is_valid= False
        if len(data['last_name']) < 2:
            flash('Last name must be at least 2 characters', 'register')
            is_valid= False
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid email address",'register')
            is_valid= False
        if len(data['password']) < 8:
            flash('Password must be at least 8 characters', 'register')
            is_valid= False
        if not data['password'] == (data['confirm_password']):
            flash("password doesn't matched", 'register')
            is_valid= False
        return is_valid
    
    @staticmethod
    def validate_login(data):
        is_valid = True
        if not EMAIL_REGEX.match(data['log_email']):
            flash("Invalid email address!", "log_email")
            is_valid = False
        if len(data['log_password'])< 8:
            flash("Password must be at least 8 character", "log_password")
            is_valid = False
        return is_valid