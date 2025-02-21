# Imports
import mongoengine as me
from models.project import Project  # Import Project model
from models.user import User  # Import User model
import datetime

# Task Model
class Task(me.Document):
    title = me.StringField(required=True, max_length=200)
    description = me.StringField()
    status = me.StringField(choices=["Pendente", "Em Progresso", "Concluído"], default="Pendente")
    project = me.ReferenceField(Project, required=True)
    createdBy = me.ReferenceField(User, required=False)
    createdAt = me.DateTimeField(default=lambda: datetime.datetime.utcnow())
