from django.contrib import admin
from .models import Specialty, Company, Vacancy, Application


class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ('code', 'id', 'title', 'picture')
    pass


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'location', 'logo', 'owner')
    pass


class VacancyAdmin(admin.ModelAdmin):
    pass


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('written_username', 'written_phone', 'vacancy', 'user')
    pass


admin.site.register(Specialty, SpecialtyAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Vacancy, VacancyAdmin)
admin.site.register(Application, ApplicationAdmin)
