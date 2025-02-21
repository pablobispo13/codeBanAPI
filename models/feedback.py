# Imports
import mongoengine as me
from models.project import Project  # Import Project model
from models.user import User  # Import User model
from models.task import Task  # Import Task model
import datetime


class Feedback(me.Document):
    project = me.ReferenceField(Project, required=True)
    task = me.ReferenceField(Task, required=True)
    user = me.ReferenceField(User, required=True)
    comment = me.StringField(required=True)
    created_at = me.DateTimeField(default=datetime.utcnow)