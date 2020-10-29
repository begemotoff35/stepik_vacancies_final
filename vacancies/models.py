from django.db import models

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
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
