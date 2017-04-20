# Create your models here.
from django.db.models import CharField, DateTimeField, TextField, \
    ForeignKey, Model, CASCADE, FileField, OneToOneField, AutoField, \
    DateField
from django.conf import settings


class Profile(Model):

    user = OneToOneField(settings.AUTH_USER_MODEL, max_length=140, default='DEFAULT VALUE')
    id = AutoField(primary_key=True)
    date_joined = DateField(auto_now_add=True)
    unique_id = CharField(max_length=20)


    def __str__(self):
        return self.user.username


class Application(Model):
    name = CharField(max_length=100)
    user = ForeignKey(Profile, on_delete=CASCADE)
    description = TextField()
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Version(Model):
    LOOKUP_CHOISE = {
        'W' : 'Windows',
        'A' : 'Android',
        'I' : 'IOS'
    }
    # LOOKUP_CHOISE используется в views для получения полного имени
    VER_CHOICES = (
        ('W', 'Windows'),
        ('A', 'Android'),
        ('I', 'IOS'),
    )

    name = CharField(max_length=20)
    application = ForeignKey(Application, on_delete=CASCADE)
    path = FileField(upload_to='upload')
    ver_log = FileField(upload_to='logs')
    ver_type = CharField(max_length=1, choices=VER_CHOICES)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


