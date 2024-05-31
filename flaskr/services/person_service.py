from neomodel import db
from ..models.Person import *
from ..exceptions.person_not_valid_exception import PersonNotValidException
import re

def save_person(person:Person)->Person:
    if not is_valid_person(person):
        raise PersonNotValidException()
    return person.save()

def delete_person(uid:str):
    person = Person.nodes.get_or_none(uid = uid)
    if person:
        person.delete()

def find_person_by_uid(uid:str):
    return Person.nodes.get_or_none(uid=uid)

def find_person_by_email(email:str):
    return Person.nodes.get_or_none(email=email)

def person_knows_new_people(person:Person,people_known_by:list[Person]):
    for person_known_by in people_known_by:
        person_knows_new_person(person,person_known_by)
    return person

def person_knows_new_person(person:Person,person_known_by:Person):
    return person.knows.connect(person_known_by)

def delete_relation_knows(person:Person,not_known_person:Person):
    return person.knows.disconnect(not_known_person)

def path_to_other_person_by_knows(start_person:Person,person_to_meet:Person):
    result = db.cypher_query('MATCH p=shortestPath((:Person {uid:$uid_start_person})-[KNOWS*]->(:Person {uid:$uid_person_to_meet})) RETURN p',
                             resolve_objects=True,params={'uid_start_person':start_person.uid,'uid_person_to_meet':person_to_meet.uid})
    return result[0][0][0]

def is_valid_person(person:Person)->bool:
    if not re.fullmatch(r'[a-zA-Z ]{3,30}',person.name,re.I):
        return False
    if not re.fullmatch(r'[a-zA-Z ]{3,30}',person.surname,re.I):
        return False
    
    return True