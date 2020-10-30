from crispy_forms.bootstrap import FormActions
from django import forms

from django.contrib.auth.forms import UserCreationForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field

from vacancies.models import Application, Company, Vacancy, Specialty


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
        fields = ['name', 'location', 'description', 'employee_count', 'logo']

    logo = forms.ImageField(required=False)


class VacancyEditForm(forms.ModelForm):
    class Meta:
        model = Vacancy
        fields = ['title', 'specialty', 'skills', 'description', 'salary_min', 'salary_max']

    class Specialties:
        choices = [
            ('', '--- Выберите специализацию ---'),
            (Specialty.FRONTEND, 'Фронтенд разработка'),
            (Specialty.BACKEND, 'Бэкенд разработка'),
            (Specialty.GAMEDEV, 'Разработка игр'),
            (Specialty.DEVOPS, 'Девопс'),
            (Specialty.DESIGN, 'Дизайн'),
            (Specialty.PRODUCTS, 'Продукты'),
            (Specialty.MANAGEMENT, 'Менеджмент'),
            (Specialty.TESTING, 'Тестирование'),
        ]
    specialty = forms.ChoiceField(label='Специализация', choices=Specialties.choices)
    skills = forms.CharField(label="Требуемые навыки", required=False, widget=forms.Textarea(attrs={'rows': '3'}))
    description = forms.CharField(label="Описание вакансии", required=False, widget=forms.Textarea(attrs={'rows': '13'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column(Field('title', placeholder='Моя вакансия'), css_class='form-group col-12 col-md-6'),
                Column('specialty', css_class='form-group col-12 col-md-6'),
                css_class='form-row'
            ),
            Row(
                Column('salary_min', css_class='form-group col-12 col-md-6'),
                Column('salary_max', css_class='form-group col-12 col-md-6'),
                css_class='form-row'
            ),
            'skills',
            'description',

            FormActions(
                Submit('submit', 'Сохранить', css_class="btn-info"),
            )
        )

        self.fields['title'].label = 'Название вакансии'
        self.fields['salary_min'].label = 'Зарплата от'
        self.fields['salary_max'].label = 'Зарплата до'

        # self.fields['specialty'].initial = Specialty.BACKEND
