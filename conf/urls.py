"""conf URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static
from django.urls import include

from django.contrib.auth.views import LogoutView

import vacancies.views as views

import debug_toolbar

urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include(debug_toolbar.urls)),
    path('', views.MainView.as_view(), name='main'),
    path('vacancies/', views.VacanciesView.as_view(), name='all_vacancies'),
    path('vacancies/cat/<slug:speciality_code>/', views.VacanciesView.as_view(), name='vacancies_by_speciality'),
    # re_path(r'^vacancies/?(cat/(?P<speciality_code>\w+))?/$', VacanciesView.as_view()),
    path('vacancies/<int:vacancy_id>/', views.VacancyView.as_view(), name='vacancy_info'),
    path('vacancies/<int:vacancy_id>/sent', views.VacancySent.as_view(), name='vacancy_sent'),
    path('companies/<int:company_id>/', views.CompanyView.as_view(), name='company_vacancies'),
    path('mycompany/', views.UserCompanyView.as_view(), name='user_company'),
    path('mycompany/create', views.create_user_company, name='user_company_create'),
    path('mycompany/profile', views.user_profile, name='user_profile'),
    path('login', views.MyLoginView.as_view(), name='login'),
    path('register', views.MySignupView.as_view(), name='register'),
    path('logout', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
