from django.forms import ModelForm
from IMDB_user.models import MyCustomUser


class UserForm(ModelForm):
    class Meta:
        model= MyCustomUser
        fields =[ 
            'bio',
            'displayname',
            'profile_pic'
        ]