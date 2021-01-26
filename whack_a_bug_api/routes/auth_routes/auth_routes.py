from . import auth
from flask.views import MethodView
from whack_a_bug_api.db import db
from flask import jsonify, make_response, request, abort
from whack_a_bug_api.models.users import User
from flask_login import login_user

class RegisterView(MethodView):
    """Class controlling api route for registering a new user"""
    
    def post(self):
        form_data = request.get_json()
        
        user = User(
            first_name = form_data.get('first_name'),
            last_name = form_data.get('last_name'),
            email = form_data.get('email'),
            role_id = form_data.get('role_id')
        )
        
        try: 
            user.set_password(form_data.get('password'))
            db.session.add(user)
            db.session.commit()
            
            res = {'message': 'User registered successfully!'}
            return make_response(jsonify(res), 201)
        except AssertionError as e:
            res = {'message': '{}'.format(str(e))}
            return make_response(jsonify(res), 401)
        

class LoginView(MethodView):
    """Class controlling api route for user authentication"""
    
    def post(self):
        form_data = request.get_json()
        email = form_data.get('email')
        password = form_data.get('password')
        
        try:
            user = User.query.filter_by(email = email).first()
            
            #check if user exists and if password is correct
            if user and user.check_password(password):
                #create access token
                access_token = user.generate_token(user.public_id)
                
                #if access token is generated
                if access_token:
                    res = {
                        'message': 'Login Successful!',
                        'access_token': access_token
                    }
                    
                    login_user(user)
                    return make_response(jsonify(res), 200)
            else:
                #user does not exist
                res = {'message': 'email or password does not exist!'}
                return make_response(jsonify(res), 402)
        except AssertionError as e:
            res = {'message': '{}'.format(str(e))}
            return make_response(jsonify(res), 401)
        
# define auth routes
register_view = RegisterView.as_view('register_view')
login_view = LoginView.as_view('login_view')

# create url rules for endpoints
auth.add_url_rule(
    '/api/auth/register',
    view_func=register_view
)
auth.add_url_rule(
    '/api/auth/login',
    view_func=login_view
)