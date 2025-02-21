import mongoengine as me

class Column(me.EmbeddedDocument):
    name = me.StringField(required=True)
    status = me.StringField(required=True)

class Board(me.Document):
    name = me.StringField(required=True)
    columns = me.EmbeddedDocumentListField(Column)  
    project = me.ReferenceField('Project', unique=True, required=True)  # Usando string aqui
