# Заполняем нашу базу данных в соответствии с данными из файла data.py

import os
import django

os.environ["DJANGO_SETTINGS_MODULE"] = 'conf.settings'
django.setup()  # Всякие Django штуки импортим после сетапа

from datetime import datetime

from vacancies.data import jobs, companies, specialties
from vacancies.models import Vacancy, Company, Specialty

if __name__ == '__main__':
    print('Please wait...', end='')

    # заполняем специальности:
    for spec in specialties:
        Specialty.objects.update_or_create(code=spec['code'], title=spec['title'], picture=spec['picture'])

    # заполняем компании:
    for company in companies:
        Company.objects.update_or_create(name=company['title'],
                                         location=company['location'],
                                         logo=company['logo'],
                                         description=company['description'],
                                         employee_count=company['employee_count'],
                                         )

    # заполняем вакансии:
    for vacancy in jobs:
        specialty = Specialty.objects.filter(code=vacancy['cat']).first()
        company = Company.objects.filter(name=vacancy['company']).first()
        Vacancy.objects.update_or_create(title=vacancy['title'],
                                         specialty=specialty,
                                         company=company,
                                         description=vacancy['desc'],
                                         salary_min=vacancy['salary_from'],
                                         salary_max=vacancy['salary_to'],
                                         published_at=datetime.strptime(vacancy['posted'], '%Y-%m-%d'),
                                         )
    print('ok')
