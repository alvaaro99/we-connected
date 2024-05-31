from flask import Blueprint, request, jsonify
from .services import person_service
from flask_jwt_extended import jwt_required,get_jwt_identity
from .models.Person import Person
from flask_jwt_extended.exceptions import NoAuthorizationError
from datetime import datetime
from neomodel.exceptions import UniqueProperty
from .exceptions.user_cannot_create_other_person import UserCannotCreateOtherPerson
from neomodel import StructuredRel

person_bp = Blueprint('person', __name__,url_prefix='/person')

@person_bp.route('/me', methods=(['GET']))
@jwt_required()
def get_my_person():
    person:Person = person_service.find_person_by_email(get_jwt_identity()[1])
    return jsonify(person.to_dict_with_all_relations())


@person_bp.route('/create', methods=(['POST']))
@jwt_required()
def create_person():
    data_request:dict = request.get_json()
    email_user = get_jwt_identity()[1]
    if 'email' in data_request.keys() and email_user != data_request['email']:
        raise UserCannotCreateOtherPerson()
    data_request['birthday'] = datetime.strptime(data_request['birthday'],'%d/%m/%Y') 
    new_person = Person(name=data_request['name'],surname=data_request['surname'],birthday=data_request['birthday'],email=email_user,gender=data_request['gender'])
    try:
        new_person = person_service.save_person(new_person)
    except UniqueProperty:
        raise UniqueProperty('Person already exists')
    if 'known_people_emails' in data_request.keys():
        known_people = [person_service.find_person_by_email(email) for email in data_request['email_people']]
        person_service.person_knows_new_people(new_person, known_people)

    return jsonify(new_person.to_dict_just_me())

@person_bp.route('/delete-relation', methods=(['DELETE']))
@jwt_required()
def delete_relation():
    data_request:dict = request.get_json()
    person = person_service.find_person_by_email(data_request['email_person'])

    not_known_people = [person_service.find_person_by_email(email) for email in data_request['email_people']]

    for not_known_person in not_known_people:
        person_service.delete_relation_knows(person, not_known_person)
    
    return jsonify({'message':'deleted'}),201


@person_bp.route('/create-relation', methods=(['POST']))
@jwt_required()
def create_relation():
    data_request:dict = request.get_json()
    person = person_service.find_person_by_email(data_request['email_person'])

    known_people = [person_service.find_person_by_email(email) for email in data_request['email_people']]

    person_service.person_knows_new_people(person, known_people)
    
    return jsonify({'message':'Created'}),201


@person_bp.route('/get-path', methods=(['POST']))
@jwt_required()
def get_path_to_other():
    data_request:dict = request.get_json()
    start_person = person_service.find_person_by_email(data_request['start_email'])
    end_person = person_service.find_person_by_email(data_request['end_email'])

    path:list[Person] = person_service.path_to_other_person_by_knows(start_person,end_person)

    return jsonify({'nodes':[(person.to_dict_just_me()) for person in path.nodes],'relationships':relations_to_list(path.relationships)})


def relations_to_list(relations:list[StructuredRel]):
    return [{'start_node':relation.start_node().to_dict_just_me(),'end_node':relation.end_node().to_dict_just_me()} for relation in relations]


@person_bp.errorhandler(NoAuthorizationError)
def no_auth_exception(_: NoAuthorizationError):
    response = jsonify({'message':'Login required'})
    response.status_code = 403
    return response


@person_bp.errorhandler(UserCannotCreateOtherPerson)
def no_auth_exception(error: UserCannotCreateOtherPerson):
    response = jsonify({'message':error.message})
    response.status_code = error.status_code
    return response


@person_bp.errorhandler(UniqueProperty)
def person_exists(error:UniqueProperty):
    response = jsonify({'message':error.message})
    response.status_code = 400
    return response


@person_bp.errorhandler(500)
def default_exception(error):
    print(type(error))
    response = jsonify({'message':error})
    response.status_code = 500
    return response