# Generated by Django 3.1.6 on 2021-02-18 20:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20210218_1952'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='application',
            name='org_id',
        ),
    ]
