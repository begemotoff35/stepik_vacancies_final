# Generated by Django 3.1.2 on 2020-10-30 15:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vacancies', '0005_auto_20201029_1405'),
    ]

    operations = [
        migrations.CreateModel(
            name='Resume',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('surname', models.CharField(blank=True, max_length=100)),
                ('status', models.CharField(choices=[('NLJ', 'Не ищу работу'), ('COF', 'Рассматриваю предложения'), ('LOJ', 'Ищу работу')], max_length=3)),
                ('salary', models.DecimalField(decimal_places=0, max_digits=10)),
                ('grade', models.CharField(choices=[('I', 'Стажер'), ('J', 'Джуниор'), ('M', 'Миддл'), ('S', 'Синьор'), ('L', 'Лид')], max_length=1)),
                ('education', models.TextField(max_length=1000)),
                ('experience', models.TextField(max_length=1000)),
                ('portfolio', models.CharField(blank=True, max_length=100)),
                ('specialty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resumes', to='vacancies.specialty')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='resume', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]