# Generated by Django 3.1.7 on 2021-02-25 23:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20210225_2335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicant',
            name='building_no',
            field=models.IntegerField(default=0, verbose_name='Building No'),
        ),
        migrations.AlterField(
            model_name='applicant',
            name='flat_no',
            field=models.IntegerField(default=0, verbose_name='Flat No'),
        ),
        migrations.AlterField(
            model_name='applicant',
            name='road_no',
            field=models.IntegerField(default=0, verbose_name='Road No'),
        ),
    ]
