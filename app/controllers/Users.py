"""
    Sample Controller File

    A Controller should be in charge of responding to a request.
    Load models to interact with the database and load views to render them to the client.

    Create a controller using this template
"""
from flask import Flask, session, Markup, flash
import random
import requests

from system.core.controller import *
from time import strftime
import string
import pprint
string.letters
'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
import random
random.choice(string.letters)
# from flask.ext.bcrypt import Bcrypt
# bcrypt = Bcrypt(app)
class Users(Controller):
    def __init__(self, action):
        super(Users, self).__init__(action)
        self.load_model('User')
        """
            This is an example of loading a model.
            Every controller has access to the load_model method.

            self.load_model('WelcomeModel')
        """

    """ This is an example of a controller method that will load a view for the client """

    def index(self):
        """ 
        A loaded model is accessible through the models attribute 
        self.models['WelcomeModel'].get_all_users()
        """
        return self.load_view('index.html')

    def register(self):
        usery = {
            "first_name" : request.form['first_name'],
            "last_name" : request.form['last_name'],
            "email" : request.form['email'],
            "password" : request.form['password'],
            "confirm_password" : request.form['confirm_password']
        }

        user_status = self.models['User'].create(usery)
        if (user_status['status'] == True):
            session['id'] = user_status['user']['id']
            session['first_name'] = user_status['user']['first_name']
            return redirect('/users/success_load')
        else:
            for message in user_status['errors']:
                flash(message, 'regis_errors')
            return redirect('/')
    
    def login(self):
        user_login = {
            "email" : request.form['email'],
            "password" : request.form['password']
        }

        login_status = self.models['User'].get_by_email(user_login)
        if (login_status['status'] == True):
            session['id'] = login_status['user']['id']
            session['first_name'] = login_status['user']['first_name']
            return redirect('/users/success_load')
        else:
            for message in user_status['errors']:
                flash(message, 'regis_errors')
            return redirect('/')

    def success_load(self):
        return self.load_view('success2.html')
    def go_back(self):
        return redirect('/')

    def reset(self):
        session.clear()
        return redirect('/')
