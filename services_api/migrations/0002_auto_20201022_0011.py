# Generated by Django 3.1.2 on 2020-10-22 00:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services_api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='icon',
            field=models.CharField(max_length=100),
        ),
    ]
