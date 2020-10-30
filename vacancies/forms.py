from crispy_forms.bootstrap import FormActions
from django import forms

from django.contrib.auth.forms import UserCreationForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field

from vacancies.models import Application, Company, Vacancy, Specialty, Resume


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
        fields = ['title', 'skills', 'description', 'salary_min', 'salary_max']

    form_specialty = forms.ChoiceField(label='Специализация', choices=Specialty.CHOICES)
    skills = forms.CharField(label="Требуемые навыки", required=False, widget=forms.Textarea(attrs={'rows': '3'}))
    description = forms.CharField(label="Описание вакансии", required=False,
                                  widget=forms.Textarea(attrs={'rows': '13'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column(Field('title', placeholder='Моя вакансия'), css_class='form-group col-12 col-md-6'),
                Column('form_specialty', css_class='form-group col-12 col-md-6'),
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


class ResumeEditForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['name', 'surname', 'status', 'salary', 'grade', 'education', 'experience', 'portfolio']

    form_specialty = forms.ChoiceField(label='Специализация', choices=Specialty.CHOICES)
    education = forms.CharField(label="Образование", required=False,
                                widget=forms.Textarea(attrs={'rows': '4'}))  # и как сюда добавить text-uppercase ??
    experience = forms.CharField(label="Опыт работы", required=False,
                                 widget=forms.Textarea(attrs={'rows': '4'}))

    # <label class="mb-2 text-dark" for="{{ form.education.id_for_label }}">Образование</label> <textarea
    # class="form-control text-uppercase" rows="4" id="{{ form.experience.id_for_label }}" style="color:#000;"
    # name="{{ form.experience.html_name }}" > < / textarea >

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].label = 'Имя'
        self.fields['surname'].label = 'Фамилия'
        self.fields['salary'].label = 'Ожидаемое вознаграждение'
        self.fields['status'].label = 'Готовность к работе'
        self.fields['grade'].label = 'Квалификация'

        self.fields['portfolio'].label = 'Ссылка на портфолио'

