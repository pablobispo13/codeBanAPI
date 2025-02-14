# Imports
import mongoengine as me
import datetime

# User Model
class User(me.Document):
    name = me.StringField(required=True, max_length=100)
    email = me.EmailField(required=True, unique=True)
    pass_hash = me.StringField(required=True)  
    totp_secret = me.StringField(required=True)
    createdAt = me.DateTimeField(default=lambda: datetime.datetime.utcnow())
