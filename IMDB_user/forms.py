from django.forms import ModelForm
from IMDB_user.models import MyCustomUser


class DisplaynameForm(ModelForm):
    class Meta:
        model = MyCustomUser
        fields = [
            'displayname',
        ]


class ProfilePicForm(ModelForm):
    class Meta:
        model = MyCustomUser
        fields = [
            'profile_pic',
        ]


class BioForm(ModelForm):
    class Meta:
        model = MyCustomUser
        fields = [
            'bio',
        ]
