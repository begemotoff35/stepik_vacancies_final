from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class LoginForm(forms.Form):
    login = forms.CharField(min_length=2)
    password = forms.CharField(min_length=6)
    test = forms.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Войти'))
