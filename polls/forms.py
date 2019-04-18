from django import forms

class NameForm(forms.Form):
    username = forms.CharField(label="User Name" , max_length=100)
    password = forms.CharField(label="Password" , max_length=100)


class Profiles(forms.Form):
    names = forms.CharField(label="names" , max_length=100)
    locations = forms.CharField(label="Locations" , max_length=100)


