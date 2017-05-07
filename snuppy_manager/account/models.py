# Create your models here.
from django.db.models import CharField, DateTimeField, TextField, \
    ForeignKey, Model, CASCADE, FileField, OneToOneField, AutoField, \
    DateField, URLField, ManyToManyField
from django.conf import settings


class Profile(Model):

    user = OneToOneField(settings.AUTH_USER_MODEL, max_length=140, default='DEFAULT VALUE')
    id = AutoField(primary_key=True)
    date_joined = DateField(auto_now_add=True)
    unique_id = CharField(max_length=20)


    def __str__(self):
        return self.user.username

    @staticmethod
    def check_profile(username):
        try:
            profile = Profile.objects.get(user__username=username)
        except: # НУЖНО ДОБАВИТЬ DoesNotExist
            profile = None
        finally:
            return profile


class Group(Model):

    name = CharField(max_length=32)

    profile = ManyToManyField(Profile, through='Rule')

    def __str__(self):
        return self.name


class Application(Model):
    name = CharField(max_length=100)
    group = ForeignKey(Group, on_delete=CASCADE)
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


class Rule(Model):

    RULE_CHOICES = (
        ('A', 'Admin'),
        ('M', 'Manager'),
        ('G', 'Guest'),
        ('U', 'UserDefine'),
    )

    group = ForeignKey(Group) #on_delete??
    profile = ForeignKey(Profile) #on_delete??
    rule = CharField(max_length=1, choices=RULE_CHOICES)

    @property
    def username(self):
        return self.profile.user.username

    @property
    def other_choices(self):
        return [ rule_type for rule_type in self.RULE_CHOICES if rule_type[1] != self.get_rule_display and rule_type[0] != 'U' ]


class Invite(Model):

    profile = ForeignKey(Profile, on_delete=CASCADE)
    group = ForeignKey(Group, on_delete=CASCADE)