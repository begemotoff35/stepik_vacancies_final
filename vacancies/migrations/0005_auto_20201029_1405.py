# Generated by Django 3.1.2 on 2020-10-29 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vacancies', '0004_auto_20201029_1351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='specialty',
            name='code',
            field=models.SlugField(unique=True),
        ),
    ]