from django.db import models

from django.contrib.auth import get_user_model

from django.utils.translation import gettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField

from conf.settings import MEDIA_COMPANY_IMAGE_DIR, MEDIA_SPECIALITY_IMAGE_DIR


class Specialty(models.Model):
    FRONTEND = 'frontend'
    BACKEND = 'backend'
    GAMEDEV = 'gamedev'
    DEVOPS = 'devops'
    DESIGN = 'design'
    PRODUCTS = 'products'
    MANAGEMENT = 'management'
    TESTING = 'testing'

    CHOICES = [
        (None, '--- Выберите специализацию ---'),
        (FRONTEND, 'Фронтенд разработка'),
        (BACKEND, 'Бэкенд разработка'),
        (GAMEDEV, 'Разработка игр'),
        (DEVOPS, 'Девопс'),
        (DESIGN, 'Дизайн'),
        (PRODUCTS, 'Продукты'),
        (MANAGEMENT, 'Менеджмент'),
        (TESTING, 'Тестирование'),
    ]

    code = models.SlugField(unique=True)
    title = models.CharField(max_length=100)
    picture = models.ImageField(upload_to=MEDIA_SPECIALITY_IMAGE_DIR)

    def __str__(self):
        return f'{self.code}'


class Company(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    logo = models.ImageField(upload_to=MEDIA_COMPANY_IMAGE_DIR)
    description = models.TextField(max_length=200)
    employee_count = models.IntegerField()
    owner = models.OneToOneField(get_user_model(),
                                 on_delete=models.PROTECT, null=True, blank=True, related_name='company')

    def __str__(self):
        return f'{self.name}'


class Vacancy(models.Model):
    title = models.CharField(max_length=100)
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, related_name='vacancies')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='vacancies')
    skills = models.CharField(max_length=100, blank=True)
    description = models.TextField(max_length=200, blank=True)
    salary_min = models.DecimalField(decimal_places=2, max_digits=15, blank=True)
    salary_max = models.DecimalField(decimal_places=2, max_digits=15, blank=True)
    published_at = models.DateField(auto_now=True)

    def __str__(self):
        return f'{self.title} - {self.specialty} - {self.company}'


class Application(models.Model):
    written_username = models.CharField(max_length=100)
    written_phone = PhoneNumberField()
    written_cover_letter = models.TextField()
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name='applications')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='applications')


class JobSearchStatus(models.TextChoices):
    NOT_LOOKING_JOB = 'NLJ', _('Не ищу работу')
    CONSIDERING_OFFERS = 'COF', _('Рассматриваю предложения')
    LOOKING_JOB = 'LOJ', _('Ищу работу')


class Grade(models.TextChoices):
    INTERN = 'I', _('Стажер')
    JUNIOR = 'J', _('Джуниор')
    MIDDLE = 'M', _('Миддл')
    SENIOR = 'S', _('Синьор')
    LEADER = 'L', _('Лид')


class Resume(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='resume')
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=3, choices=JobSearchStatus.choices)
    salary = models.DecimalField(decimal_places=0, max_digits=10)
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, related_name='resumes',
                                  choices=Specialty.CHOICES, max_length=10)
    grade = models.CharField(max_length=1, choices=Grade.choices)
    education = models.TextField(max_length=1000, blank=True)
    experience = models.TextField(max_length=1000, blank=True)
    portfolio = models.CharField(max_length=100, blank=True)
