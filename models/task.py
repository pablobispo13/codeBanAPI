# Imports
import mongoengine as me
from .project import Project  # Import Project model
from .user import User  # Import User model
import datetime

# Task Model
class Task(me.Document):
    title = me.StringField(required=True, max_length=200)
    description = me.StringField()
    status = me.StringField(choices=["Pendente", "Em Progresso", "Concluído"], default="Pendente")
    project = me.ReferenceField(Project, required=True)
    user = me.ReferenceField(User, required=False)
    createdAt = me.DateTimeField(default=lambda: datetime.datetime.utcnow())
