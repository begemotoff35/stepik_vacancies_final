from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404

from django.db.models import Count
from django.http import Http404, HttpResponse
from django.urls import reverse

from django.views.generic.base import TemplateView, View
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm

from conf import settings
from vacancies.forms import MyRegisterForm, ApplicationForm, CompanyForm
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


class UserCompanyView(View):
    def get(self, request):
        user = self.request.user
        company = Company.objects.filter(owner=user).first()
        if company is None:
            company = Company.objects.create(owner=user,
                                             employee_count=0)
        template_name = 'company-create.html' if company is None else 'company-edit.html'
        template_name = 'vacancies/' + template_name
        return render(request, template_name, {'company': company, 'title_left': 'Моя компания'})

    def post(self, request):
        user = self.request.user
        company = Company.objects.filter(owner=user).first()
        form = CompanyForm(request.POST)
        if form.is_valid():
            if company is not None:
                data = form.cleaned_data
                company.name = data['name']
                company.location = data['location']
                # company.logo = data['logo']
                company.description = data['description']
                company.employee_count = data['employee_count']
                company.save()
            return redirect(reverse('user_company'))
        return render(request, 'vacancies/company-edit.html', {'form': form, 'company': company})


class MyLoginView(LoginView):
    template_name = "vacancies/login.html"
    # redirect_authenticated_user = False
    form_class = AuthenticationForm

    def post(self, request):
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
                    return redirect(self.success_url)
            else:
                return redirect(reverse('login'))
        return render(request, self.template_name, {'form': form})
