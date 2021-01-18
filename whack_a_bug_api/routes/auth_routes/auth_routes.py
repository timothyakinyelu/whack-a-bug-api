from . import auth
from flask.views import MethodView
from whack_a_bug_api.db import db
from flask import jsonify, make_response, request, abort
from whack_a_bug_api.models.users import User

class RegisterView(MethodView):
    """Class controlling all api routes for authentication"""
    
    def post(self):
        form_data = request.get_json()
        
        user = User(
            first_name = form_data.get('first_name'),
            last_name = form_data.get('last_name'),
            email = form_data.get('email'),
            password = form_data.get('password')
        )
        
        try: 
            db.session.add(user)
            db.session.commit()
            
            res = {'message': 'User registered successfully!'}
            return make_response(jsonify(res), 201)
        except AssertionError as e:
            res = {'message': '{}'.format(str(e))}
            return make_response(jsonify(res), 401)
        
        
# define user routes
register_view = RegisterView.as_view('register_view')

# create url rules for endpoints
auth.add_url_rule(
    '/api/auth/users',
    view_func=register_view
)