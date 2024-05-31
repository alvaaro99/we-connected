import pytest
from unittest.mock import patch, Mock

from tests.test import *
from flaskr.exceptions.user_not_valid_exception import UserNotValidException
from flaskr.exceptions.user_not_found_exception import UserNotFoundException


@patch('flaskr.services.user_service.create_user')
@patch('flaskr.services.user_service.find_user_by_email')
@patch('flaskr.auth.create_access_token')
@patch('flaskr.auth.create_refresh_token')
def test_register_successful(
    mock_create_refresh_token: Mock,
    mock_create_access_token: Mock,
    mock_find_user_by_email: Mock,
    mock_create_user: Mock, 
    client):
    
    data_request = {'email': 'test@example.com', 'password': 'password123'}
    new_user = {'id': 1, 'email': 'test@example.com'}
    
    mock_create_user.return_value = None
    mock_find_user_by_email.return_value = new_user
    mock_create_access_token.return_value = 'access_token_mock'
    mock_create_refresh_token.return_value = 'refresh_token_mock'

    response = client.post('auth/register', json=data_request)
    
    assert response.status_code == 200
    assert response.get_json() == {'access_token': 'access_token_mock', 'refresh_token': 'refresh_token_mock'}
    mock_create_user.assert_called_once()
    mock_find_user_by_email.assert_called_once_with(data_request['email'])
    mock_create_access_token.assert_called_once()
    mock_create_refresh_token.assert_called_once()

@patch('flaskr.services.user_service.create_user')
def test_register_fail(
    mock_create_user: Mock, 
    client):
    
    data_request = {'email': 'test@example.com', 'password': 'password123'}
    
    mock_create_user.side_effect = UserNotValidException()

    with pytest.raises(UserNotValidException):
        client.post('auth/register', json=data_request)


@patch('flaskr.services.user_service.find_user_by_email')
@patch('flaskr.auth.create_access_token')
@patch('flaskr.auth.create_refresh_token')
@patch('flaskr.services.user_service.is_same_password')
def test_login_successful(
    mock_is_same_password:Mock,
    mock_create_refresh_token:Mock,
    mock_create_access_token:Mock,
    mock_find_user_by_email:Mock,
    client):
    
    data_request = {'email': 'test@example.com', 'password': 'password123'}
    user = {'id': 1, 'email': 'test@example.com', 'password':'password123'}
    
    mock_find_user_by_email.return_value = user
    mock_create_access_token.return_value = 'access_token_mock'
    mock_create_refresh_token.return_value = 'refresh_token_mock'
    mock_is_same_password.return_value = True

    response = client.post('auth/login', json=data_request)
    
    assert response.status_code == 200
    assert response.get_json() == {'access_token': 'access_token_mock', 'refresh_token': 'refresh_token_mock'}
    mock_find_user_by_email.assert_called_once_with(data_request['email'])
    mock_create_access_token.assert_called_once()
    mock_create_refresh_token.assert_called_once()

@patch('flaskr.services.user_service.find_user_by_email')
@patch('flaskr.services.user_service.is_same_password')
def test_login_fail_not_user_found(
    mock_is_same_password: Mock,
    mock_find_user_by_email: Mock,
    client):
    
    data_request = {'email': 'test@example.com', 'password': 'password123'}
    
    mock_find_user_by_email.return_value = None
    mock_is_same_password.return_value = True

    with pytest.raises(UserNotFoundException):
        client.post('auth/login', json=data_request)
    mock_find_user_by_email.assert_called_once_with(data_request['email'])

@patch('flaskr.services.user_service.find_user_by_email')
@patch('flaskr.services.user_service.is_same_password')
def test_login_fail_not_same_password(
    mock_is_same_password:Mock,
    mock_find_user_by_email:Mock,
    client):
    
    data_request = {'email': 'test@example.com', 'password': 'password123'}
    user = {'id': 1, 'email': 'test@example.com', 'password':'password1234'}
    
    mock_find_user_by_email.return_value = user
    mock_is_same_password.return_value = False

    with pytest.raises(UserNotFoundException):
        client.post('auth/login', json=data_request)
    
    mock_find_user_by_email.assert_called_once_with(data_request['email'])