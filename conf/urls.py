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
from django.contrib import admin
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static
from django.urls import include

from vacancies.views import MainView, VacanciesView, VacancyView, CompanyView

import debug_toolbar

urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include(debug_toolbar.urls)),
    path('', MainView.as_view(), name='main'),
    path('vacancies/', VacanciesView.as_view(), name='all_vacancies'),
    path('vacancies/cat/<slug:speciality_code>/', VacanciesView.as_view(), name='vacancies_by_speciality'),
    # re_path(r'^vacancies/?(cat/(?P<speciality_code>\w+))?/$', VacanciesView.as_view()),
    path('vacancies/<int:vacancy_id>/', VacancyView.as_view(), name='vacancy_info'),
    path('companies/<int:company_id>/', CompanyView.as_view(), name='company_vacancies'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
