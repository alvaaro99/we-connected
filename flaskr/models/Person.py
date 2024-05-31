from neomodel import StructuredNode,StringProperty,UniqueIdProperty,DateTimeFormatProperty,EmailProperty, RelationshipTo

class Person(StructuredNode):
    uid = UniqueIdProperty()
    name =  StringProperty(required=True)
    surname =  StringProperty(required=True)
    birthday = DateTimeFormatProperty(default=None,format='%d/%m/%y')
    email = EmailProperty(required=True, unique_index=True)
    gender = StringProperty(default=None)


    last_matched_at = DateTimeFormatProperty(default_now=True,format='%d/%m/%y %H:%M')
    created_at = DateTimeFormatProperty(default_now=True,format='%d/%m/%y %H:%M')

    knows = RelationshipTo('Person','KNOWS')

    def to_dict_just_me(self):
        return {
            'uid': self.uid,
            'name': self.name,
            'surname': self.surname,
            'birthday': self.birthday.strftime('%d/%m/%y') if self.birthday else None,
            'email': self.email,
            'gender': self.gender,
            'last_matched_at': self.last_matched_at.strftime('%d/%m/%y %H:%M') if self.last_matched_at else None,
            'created_at': self.created_at.strftime('%d/%m/%y %H:%M') if self.created_at else None
        }
    
    def to_dict_with_all_relations(self):
        return {
            'uid': self.uid,
            'name': self.name,
            'surname': self.surname,
            'birthday': self.birthday.strftime('%d/%m/%y') if self.birthday else None,
            'email': self.email,
            'gender': self.gender,
            'last_matched_at': self.last_matched_at.strftime('%d/%m/%y %H:%M') if self.last_matched_at else None,
            'created_at': self.created_at.strftime('%d/%m/%y %H:%M') if self.created_at else None,
            'knows': [{'uid': person.uid, 'name': person.name} for person in self.knows.all()]
        }