# Imports
import mongoengine as me
from .user import User  # Import User model
import datetime

# Project Model
class Project(me.Document):
    name = me.StringField(required=True, max_length=200)
    description = me.StringField()
    createdBy = me.ReferenceField(User, required=True)
    createdAt = me.DateTimeField(default=lambda: datetime.datetime.utcnow())