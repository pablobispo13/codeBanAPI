import mongoengine as me
from models.user import User  # Import User model
import datetime

# Project Model
class Project(me.Document):
    name = me.StringField(required=True, max_length=200)
    description = me.StringField()
    createdBy = me.ReferenceField(User, required=True)
    is_public = me.BooleanField(default=False)
    createdAt = me.DateTimeField(default=lambda: datetime.datetime.utcnow())
    board = me.ReferenceField('Board', unique=True)  # Usando string aqui
