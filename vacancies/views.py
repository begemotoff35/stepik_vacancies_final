from django.contrib.auth import login
from django.contrib.auth.models import User

from django.shortcuts import render, redirect, get_object_or_404

from django.db.models import Count
from django.http import Http404, HttpResponse, HttpResponseServerError
from django.urls import reverse

from django.views.generic.base import TemplateView, View
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm

from vacancies.forms import MyRegisterForm, ApplicationForm, CompanyForm, VacancyEditForm
from vacancies.models import Specialty, Company, Vacancy, Application


class MainView(TemplateView):
    template_name = "vacancies/index.html"

    def get(self, request):
        specialties_with_vacancy_count = Specialty.objects.annotate(number_of_vacancies=Count('vacancies'))
        companies_with_vacancy_count = Company.objects.annotate(number_of_vacancies=Count('vacancies'))
        return render(request, self.template_name,
                      {'specialties': specialties_with_vacancy_count, 'companies': companies_with_vacancy_count})


class VacanciesView(TemplateView):
    template_name = "vacancies/vacancies.html"

    def get_context_data(self, **kwargs):
        context = super(VacanciesView, self).get_context_data(**kwargs)
        speciality_code = context.get('speciality_code', None)
        if speciality_code is None:
            vacancies = Vacancy.objects.all()
        else:
            specialty = Specialty.objects.filter(code=speciality_code).first()
            vacancies = Vacancy.objects.filter(specialty__code=speciality_code)
            if specialty is None:
                raise Http404

            context['current_specialty'] = specialty

        context['vacancies'] = vacancies
        context['title_left'] = 'Вакансии'

        return context


class VacancyView(TemplateView):
    template_name = "vacancies/vacancy.html"

    def post(self, request, vacancy_id):
        vacancy = get_object_or_404(Vacancy, id=vacancy_id)
        form = ApplicationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Application.objects.create(written_username=data['written_username'],
                                       written_phone=data['written_phone'],
                                       written_cover_letter=data['written_cover_letter'],
                                       vacancy=vacancy, user=request.user)
            return redirect(reverse('vacancy_sent', kwargs={'vacancy_id': vacancy_id}))
        return render(request, self.template_name, {'form': form, 'vacancy_id': vacancy_id, 'vacancy': vacancy})

    def get_context_data(self, vacancy_id, **kwargs):
        context = super(VacancyView, self).get_context_data(**kwargs)
        if vacancy_id is None:
            raise Http404

        vacancy = Vacancy.objects.get(id=vacancy_id)

        context['form'] = ApplicationForm()
        context['vacancy'] = vacancy
        context['title_left'] = 'Вакансия'

        return context


class VacancySent(TemplateView):
    template_name = "vacancies/sent.html"

    def get_context_data(self, vacancy_id, **kwargs):
        context = super(VacancySent, self).get_context_data(**kwargs)
        context['title_left'] = 'Отклик отправлен'
        return context


class CompanyView(TemplateView):
    template_name = "vacancies/company.html"

    def get_context_data(self, company_id, **kwargs):
        context = super(CompanyView, self).get_context_data(**kwargs)
        if company_id is None:
            raise Http404

        company = Company.objects.get(id=company_id)
        vacancies = Vacancy.objects.filter(company_id=company_id)

        context['company'] = company
        context['vacancies'] = vacancies
        context['title_left'] = 'Компания'

        return context


def user_profile(request):
    return render(request, 'vacancies/user-profile.html', {'personal_page': True})


# def create_user_key(user_id, s):
#    return f'user_{user_id}_{s}'


def create_user_company(request):
    user = request.user
    company = Company.objects.filter(owner=user).first()
    if company is None:
        # Создаём временный объект:
        company = Company(owner=user, name='')
    return render(request, 'vacancies/company-edit.html',
                  {'form': CompanyForm(), 'company': company, 'title_left': 'Моя компания'})


class UserCompanyView(View):
    def get(self, request):
        user = self.request.user
        company = Company.objects.filter(owner=user).first()
        template_name = 'vacancies/company-create.html' if company is None else 'vacancies/company-edit.html'
        return render(self.request, template_name,
                      {'form': CompanyForm(), 'company': company, 'title_left': 'Моя компания'})

    def post(self, request):
        user = self.request.user
        company = Company.objects.filter(owner=user).first()
        if company is None:
            company = Company()
        form = CompanyForm(request.POST)
        context = {'form': form, 'company': company}
        if form.is_valid():
            data = form.cleaned_data
            company.name = data['name']
            company.location = data['location']
            # Не знаю, как надо загружать logo
            # в request.POST данные есть, а в cleaned_data - нет
            # company.logo = data['logo']
            #
            # file_name = request.POST.get('logo')
            # company.logo.storage.save(file_name)
            company.description = data['description']
            company.employee_count = data['employee_count']
            company.owner = user
            company.save()
            context['info_updated'] = True
        return render(self.request, 'vacancies/company-edit.html', context)


class UserCompanyVacanciesView(TemplateView):
    template_name = 'vacancies/vacancy-list.html'

    def get_context_data(self, **kwargs):
        context = super(UserCompanyVacanciesView, self).get_context_data(**kwargs)

        user = self.request.user
        company = Company.objects.filter(owner=user).first()
        if company is None:
            raise Http404

        # Находим все вакансии по компании:
        vacancies_with_number_of_responses = \
            Vacancy.objects.filter(company=company).annotate(number_of_responses=Count('applications'))
        context['company'] = company
        context['vacancies'] = vacancies_with_number_of_responses
        context['title_left'] = 'Моя компания | Вакансии'

        return context


def create_user_vacancy(request):
    user = request.user
    # company = get_object_or_404(Company, owner=user)
    company = Company.objects.filter(owner=user).first()
    if company is None:
        raise Http404
    vacancy = Vacancy(company=company)  # 0, т.к. временный объект
    specialties = Specialty.objects.all()
    return render(request, 'vacancies/vacancy-edit.html',
                  {'form': VacancyEditForm(),
                   'vacancy': vacancy,
                   'company': company,
                   'specialties': specialties,
                   'title_left': 'Моя компания | Вакансия'})


class UserCompanyVacancyEditView(TemplateView):
    template_name = 'vacancies/vacancy-edit.html'

    def get(self, request, vacancy_id):
        user = request.user
        company = get_object_or_404(Company, owner=user)
        vacancy = Vacancy.objects.filter(id=vacancy_id).annotate(number_of_responses=Count('applications')).first()
        if vacancy is None:
            vacancy = Vacancy(company=company, specialty=None)
        applications = Application.objects.filter(vacancy=vacancy).all()

        # Вот тут я не понимаю, почему в методе get класса UserCompanyView
        #  я передаю пустую форму и в ней все поля заполнены в соответствии с моделью,
        #  а здесь форма получается пустая и приходится явно инициализировать:
        form = VacancyEditForm({'title': vacancy.title,
                                'skills': vacancy.skills,
                                # не знаю, как передать specialty в crispy form (что-то не так с чойсами)
                                # возникает ошибка ValueError
                                # Exception Value:
                                # Cannot assign "'backend'": "Vacancy.specialty" must be a "Specialty" instance.
                                # 'specialty': vacancy.specialty,
                                'description': vacancy.description,
                                'salary_min': vacancy.salary_min,
                                'salary_max': vacancy.salary_max,
                                })
        return render(request, self.template_name,
                      {'form': form,
                       'vacancy': vacancy,
                       'company': company,
                       'applications': applications,
                       'title_left': 'Моя компания | Вакансия'})

    def post(self, request, vacancy_id):
        user = request.user
        company = get_object_or_404(Company, owner=user)
        vacancy = Vacancy.objects.filter(id=vacancy_id).annotate(number_of_responses=Count('applications')).first()
        if vacancy is None:
            vacancy = Vacancy(company=company)
        applications = Application.objects.filter(vacancy=vacancy).all()
        form = VacancyEditForm(request.POST)
        context = {'form': form, 'company': company, 'vacancy': vacancy, 'applications': applications,
                   'title_left': 'Моя компания | Вакансия'}
        if form.is_valid():
            data = form.cleaned_data
            vacancy.title = data['title']
            specialty = Specialty.objects.filter(code=data['specialty']).first()
            if specialty is not None:
                vacancy.specialty = specialty
                vacancy.company = company
                vacancy.salary_min = data['salary_min']
                vacancy.salary_max = data['salary_max']
                vacancy.skills = data['skills']
                vacancy.description = data['description']
                vacancy.save()
                context['vacancy_specialty'] = data['specialty']
                context['info_updated'] = True
        return render(request, 'vacancies/vacancy-edit.html', context)


class MyLoginView(LoginView):
    template_name = 'vacancies/login.html'
    form_class = AuthenticationForm
    # redirect_authenticated_user = False
    success_url = 'user_company'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse(self.success_url))
        return super().get(request, *args, **kwargs)

    def post(self, request):
        form = self.get_form()
        if form.is_valid():
            user = form.get_user()
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect(reverse(self.success_url))
                else:
                    return HttpResponse('Disabled account')
        return render(request, self.template_name, {'form': form})


class MySignupView(CreateView):
    template_name = "vacancies/register.html"
    form_class = MyRegisterForm
    success_url = 'login'  # settings.LOGIN_REDIRECT_URL

    # redirect_authenticated_user = False

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse(self.success_url))
        return super().get(request, *args, **kwargs)

    def post(self, request):
        form = self.get_form()
        if form.is_valid():
            data = form.cleaned_data
            username, password = data['username'], data['password1']
            user = User.objects.filter(username=username, password=password).first()
            if user is None:
                # Создаём нового пользователя:
                first_name, last_name, email = data['first_name'], data['last_name'], data['email']
                user = User.objects.create_user(username=username, password=password,
                                                first_name=first_name, last_name=last_name, email=email)
                if user is not None:
                    return redirect(reverse(self.success_url))
        return render(request, self.template_name, {'form': form})
