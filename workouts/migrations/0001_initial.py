# Generated by Django 2.2 on 2019-06-04 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Training',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('exercise_category', models.CharField(max_length=10)),
                ('exercise', models.CharField(max_length=80)),
                ('set_number', models.IntegerField()),
                ('reps', models.IntegerField()),
                ('weight', models.FloatField()),
                ('rep_category', models.CharField(max_length=10)),
            ],
        ),
    ]