# Generated by Django 3.1.2 on 2020-10-30 17:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vacancies', '0007_auto_20201030_1943'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resume',
            name='specialty',
            field=models.ForeignKey(choices=[(None, '--- Выберите специализацию ---'),
                                             ('frontend', 'Фронтенд разработка'),
                                             ('backend', 'Бэкенд разработка'),
                                             ('gamedev', 'Разработка игр'), ('devops', 'Девопс'), ('design', 'Дизайн'),
                                             ('products', 'Продукты'), ('management', 'Менеджмент'),
                                             ('testing', 'Тестирование')],
                                    max_length=10, on_delete=django.db.models.deletion.CASCADE,
                                    related_name='resumes', to='vacancies.specialty'),
        ),
    ]
