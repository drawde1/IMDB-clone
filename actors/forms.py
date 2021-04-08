from django import forms

class ActorSearchForm(forms.Form):
    search_actor = forms.CharField(max_length=150)