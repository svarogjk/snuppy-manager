
from django.db.models import (CharField, Model, OneToOneField,
                              AutoField, DateField)
from django.conf import settings


#Customized User
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
