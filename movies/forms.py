from django import forms

class MovieSearchForm(forms.Form):
    search_movie = forms.CharField(max_length=150)