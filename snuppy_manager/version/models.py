from django.db.models import (CharField, DateTimeField,
    ForeignKey, Model, CASCADE, FileField)

from application.models import Application


#The version of an application you develop
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
