from django import forms

class single_music_form(forms.Form):
    music_string = forms.CharField(max_length=100)