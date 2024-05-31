from flask import Blueprint, request, jsonify
from .models.User import User
from .services import user_service
from .exceptions.user_not_found_exception import UserNotFoundException
from sqlite3 import IntegrityError
from flask_jwt_extended import create_access_token, create_refresh_token,get_jwt_identity, jwt_required

auth_bp = Blueprint('auth', __name__,url_prefix='/auth')

@auth_bp.route('/register', methods=(['POST']))
def register():
    data_request = request.get_json()
    new_user = User(data_request['email'],data_request['password'])
    try:
        user_service.create_user(new_user)
        user = user_service.find_user_by_email(new_user.email)
    except Exception as error:
        raise error
    jwt_access = create_access_token((user['id'],user['email']))
    jwt_refresh = create_refresh_token((user['id'],user['email']))
    return jsonify({'access_token':jwt_access, 'refresh_token':jwt_refresh})


@auth_bp.route('/login', methods=(['POST']))
def login():
    data_request = request.get_json()
    user = user_service.find_user_by_email(data_request['email'])
    if user is None or not user_service.is_same_password(data_request['password'], user['password']):
        raise UserNotFoundException()
    jwt_access = create_access_token((user['id'],user['email']))
    jwt_refresh = create_refresh_token((user['id'],user['email']))
    return jsonify({'access_token':jwt_access, 'refresh_token':jwt_refresh})

@auth_bp.route('/refresh', methods=(['GET']))
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    jwt_access = create_access_token(identity)
    return jsonify({'access_token':jwt_access})

@auth_bp.errorhandler(IntegrityError)
def integrity_exception(_):
    response = jsonify({'message':'Error creating user'})
    response.status_code = 400
    return response

@auth_bp.errorhandler(500)
def default_exception(_):
    response = jsonify({'message':'Unexpected error'})
    response.status_code = 500
    return response
