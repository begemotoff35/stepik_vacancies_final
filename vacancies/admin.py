from django.contrib import admin
from .models import Specialty, Company, Vacancy


class SpecialtyAdmin(admin.ModelAdmin):
    fields = ('code', 'title', 'picture')
    # readonly_fields = ('code', 'title', 'picture')
    pass


class CompanyAdmin(admin.ModelAdmin):
    pass


class VacancyAdmin(admin.ModelAdmin):
    pass


admin.site.register(Specialty, SpecialtyAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Vacancy, VacancyAdmin)
