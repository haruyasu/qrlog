# Generated by Django 3.2.6 on 2021-08-03 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='management',
            name='entered',
            field=models.DateTimeField(blank=True, null=True, verbose_name='入館'),
        ),
        migrations.AlterField(
            model_name='management',
            name='exited',
            field=models.DateTimeField(blank=True, null=True, verbose_name='退館'),
        ),
    ]
