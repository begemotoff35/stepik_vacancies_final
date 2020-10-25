from django import forms
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User

# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import Submit
from vacancies.models import Application, Company


class MyRegisterForm(UserCreationForm):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    email = forms.EmailField(required=False)


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['written_username', 'written_phone', 'written_cover_letter']


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'location', 'description', 'employee_count']
