# Create your models here.
from django.db.models import CharField, DateTimeField, TextField, \
    ForeignKey, Model, CASCADE, FileField

class User(Model):
    name = CharField(max_length=100)

    def __str__(self):
        return self.name

class Application(Model):
    name = CharField(max_length=100)
    user = ForeignKey(User, on_delete=CASCADE)
    description = TextField()
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Version(Model):
    name = CharField(max_length=20)
    application = ForeignKey(Application, on_delete=CASCADE)
    path = FileField(upload_to='upload')
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    def __str__(self):
        return self.name