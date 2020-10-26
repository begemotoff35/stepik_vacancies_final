from django import forms
from django.contrib.auth.forms import UserCreationForm

from vacancies.models import Application, Company, Vacancy


class MyRegisterForm(UserCreationForm):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    email = forms.EmailField(required=False)


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['written_username', 'written_phone', 'written_cover_letter']


class CompanyForm(forms.ModelForm):
    employee_count = forms.IntegerField(required=False, min_value=0)

    class Meta:
        model = Company
        fields = ['name', 'location', 'description', 'employee_count']


class VacancyEditForm(forms.ModelForm):
    class Meta:
        model = Vacancy
        fields = ['title', 'specialty', 'skills', 'description', 'salary_min', 'salary_max']
