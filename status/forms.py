from django import forms

class DarkTheme(forms.Form):
    night_theme = forms.BooleanField(required=False)