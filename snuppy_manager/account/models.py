# Create your models here.
from django.db.models import CharField, DateTimeField, TextField, \
    ForeignKey, Model, CASCADE, FileField, OneToOneField, AutoField, \
    DateField, URLField
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
    source_code = URLField()
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

    STATUS_CHOICES = (
        ('T', 'Translated'),
        ('C', 'Compiled'),
        ('E', 'Error'),
        ('U', 'Underway')
    )

    number = CharField(max_length=20)
    application = ForeignKey(Application, on_delete=CASCADE)
    path = FileField(upload_to='upload')
    # changes = FileField(upload_to='logs', blank=True) #blank=True temporary solution
    changes = CharField(max_length=200, blank=True)
    ver_type = CharField(max_length=1, choices=VER_CHOICES)
    status = CharField(max_length=1, choices=STATUS_CHOICES)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    def __str__(self):
        return self.number


