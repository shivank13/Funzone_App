# Generated by Django 4.0.3 on 2022-03-22 08:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CoreApp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employeeanswer',
            old_name='employee',
            new_name='student',
        ),
    ]
