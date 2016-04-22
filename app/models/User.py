""" 
    Sample Model File

    A Model should be in charge of communicating with the Database. 
    Define specific model method that query the database for information.
    Then call upon these model method in your controller.

    Create a model using this template.
"""
from system.core.model import Model
import re
from flask import flash
class User(Model):
    def __init__(self):
        super(User, self).__init__()

    def create(self, data):
        EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')
        errors = []

        if not data['first_name']:
            errors.append('first name cannot be blank')
        elif len(data['first_name']) < 2:
            errors.append('Your first name is too short')

        if not data['last_name']:
            errors.append('last name cannot be blank')
        elif len(data['last_name']) < 2:
            errors.append('Your last name is too short')

        if not data['email']:
            errors.append('Email cannot be blank')
        elif not EMAIL_REGEX.match(data['email']):
            errors.append('Email format must be valid!')
        if not data['password']:
            errors.append('Password cannot be blank')
        elif len(data['password']) < 8:
            errors.append('Your password must be at least 8 characters long')
        elif data['password'] != data['confirm_password']:
            errors.append('Password and confirmation must match')

        if errors:
            return {'status': False, 'errors': errors}
        else:
            hashed_pw = self.bcrypt.generate_password_hash(data['password'])
            create_user = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%s,%s,%s,%s, NOW(), NOW())"
            data = [data['first_name'], data['last_name'], data['email'], hashed_pw]
            self.db.query_db(create_user, data)
            
            get_user = "SELECT * FROM users ORDER BY id LIMIT 1"
            user = self.db.query_db(get_user)
            return {'status' : True, 'user' : user[0]}

    def get_by_email(self, data):
        EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')
        errors = []
        # hashed_pw = self.bcrypt.generate_password_hash(data['password'])
        if not data['email']:
            errors.append('Email cannot be blank')
        elif not EMAIL_REGEX.match(data['email']):
            errors.append('Email format must be valid!')
        if not data['password']:
            errors.append('Password cannot be blank')
        elif len(data['password']) < 8:
            errors.append('Your password must be at least 8 characters long')
            
        if errors:
            return {'status': False, 'errors': errors}
        else:
            query = "SELECT * FROM users WHERE email = %s LIMIT 1"
            pickles = [data['email']]
            user = self.db.query_db(query, pickles)
            if self.bcrypt.check_password_hash(user[0]['password'], data['password']):
                flash(u'You have successfully logged onto the page.  Thank you','success') 
                return {'status' : True, 'user' : user[0]}
    """
    Below is an example of a model method that queries the database for all users in a fictitious application

    def get_all_users(self):
        return self.db.query_db("SELECT * FROM users")

    def get_course_by_id(self, course_id):
        # pass data to the query like so
        query = "SELECT * FROM courses WHERE id = %s"
        data = [course_id]
        return self.db.query_db(query, data)

    Every model has access to the "self.db.query_db" method which allows you to interact with the database
    """

    """
    If you have enabled the ORM you have access to typical ORM style methods.
    See the SQLAlchemy Documentation for more information on what types of commands you can run.
    """
