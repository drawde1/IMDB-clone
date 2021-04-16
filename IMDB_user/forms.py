from django.forms import ModelForm
from IMDB_user.models import MyCustomUser


class DisplaynameForm(ModelForm):
    class Meta:
        model= MyCustomUser
        fields =[ 
            'displayname',
        ]

class BioForm(ModelForm):
    class Meta:
        model= MyCustomUser
        fields =[ 
            'bio',
        ]

class PhotoForm(ModelForm):
    class Meta:
        model= MyCustomUser
        fields =[ 
            'profile_pic'
        ]