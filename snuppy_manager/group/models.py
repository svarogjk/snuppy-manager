from django.db.models import (CharField, ForeignKey, Model,
                              CASCADE, ManyToManyField)

from account.models import Profile


#The group of users
class Group(Model):

    name = CharField(max_length=32)

    profile = ManyToManyField(Profile, through='Rule')

    def __str__(self):
        return self.name

    @staticmethod
    def get_user_groups(user_id):
        profile = Profile.objects.get(id=user_id)
        groups = Group.objects.filter(profile__id=profile.id)
        return groups

    @staticmethod
    def is_user_in_group(profile, group_id):
        for group in profile.group_set.values():
            if group['id'] == group_id:
                return True
        return False

    @staticmethod
    def is_user_admin_in_group(profile, group_id):
        for rule in profile.rule_set.values():
            if rule['group_id'] == group_id and rule['rule'] == 'A':
                return True
        return False


class Rule(Model):

    RULE_CHOICES = (
        ('A', 'Admin'),
        ('M', 'Manager'),
        ('G', 'Guest'),
        ('U', 'UserDefine'),
    )

    CHECK_VALUE = ('A', 'M', 'G', 'stay', 'remove', )

    group = ForeignKey(Group) #on_delete??
    profile = ForeignKey(Profile) #on_delete??
    rule = CharField(max_length=1, choices=RULE_CHOICES)

    @staticmethod
    def is_rule_exist(input_rule):
        if input_rule in Rule.CHECK_VALUE:
            return True
        return False

    @property
    def username(self):
        return self.profile.user.username

    @property
    def other_choices(self):
        return [ rule_type for rule_type in self.RULE_CHOICES if rule_type[1] != self.get_rule_display and rule_type[0] != 'U' ]


class Invite(Model):

    profile = ForeignKey(Profile, on_delete=CASCADE)
    group = ForeignKey(Group, on_delete=CASCADE)

    @staticmethod
    def is_user_have_invite(profile, group_id):
        for invite in profile.invite_set.values():
            if invite['group_id'] == group_id:
                return True
        return False
