from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from django.db.models import Count
from django.http import Http404, HttpResponse
from django.urls import reverse

from django.views.generic.base import TemplateView
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm

from conf import settings
from vacancies.forms import MyRegisterForm
from vacancies.models import Specialty, Company, Vacancy


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

    def get_context_data(self, vacancy_id, **kwargs):
        context = super(VacancyView, self).get_context_data(**kwargs)
        if vacancy_id is None:
            raise Http404

        vacancy = Vacancy.objects.get(id=vacancy_id)

        context['vacancy'] = vacancy
        context['title_left'] = 'Вакансия'

        return context


class CompanyView(TemplateView):
    template_name = "vacancies/company.html"

    def get_context_data(self, company_id, **kwargs):
        context = super(CompanyView, self).get_context_data(**kwargs)
        # company_id = context.get('company_id', None)
        if company_id is None:
            raise Http404

        company = Company.objects.get(id=company_id)
        vacancies = Vacancy.objects.filter(company_id=company_id)

        context['company'] = company
        context['vacancies'] = vacancies
        context['title_left'] = 'Компания'

        return context


"""def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data['username'], password=data['password'])
            if user is None:
                return HttpResponse('Invalid login')
            else:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
    else:
        form = AuthenticationForm()
    return render(request, 'vacancies/login.html', {'form': form})
"""


class MyLoginView(LoginView):
    template_name = "vacancies/login.html"
    # redirect_authenticated_user = False
    form_class = AuthenticationForm

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            user = form.get_user()
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect(self.get_success_url())
                else:
                    return HttpResponse('Disabled account')
        return render(request, self.template_name, {'form': form})


class MySignupView(CreateView):
    template_name = "vacancies/register.html"
    form_class = MyRegisterForm
    success_url = settings.LOGIN_REDIRECT_URL

    # redirect_authenticated_user = False

    def post(self, request, *args, **kwargs):
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
                    return redirect(self.success_url)
            else:
                return redirect(reverse('login'))
        return render(request, self.template_name, {'form': form})
