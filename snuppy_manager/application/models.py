from django.db.models import (CharField, DateTimeField, TextField,
    ForeignKey, Model, CASCADE, URLField)
from group.models import Group


#The application you develop
class Application(Model):
    name = CharField(max_length=100)
    group = ForeignKey(Group, on_delete=CASCADE)
    description = TextField()
    source_code = URLField()
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

