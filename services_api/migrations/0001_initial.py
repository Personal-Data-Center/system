# Generated by Django 3.1.2 on 2020-10-20 23:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('docker_id', models.CharField(max_length=30)),
                ('super', models.BooleanField(blank='false')),
                ('is_required', models.BooleanField(blank='false')),
                ('path', models.CharField(max_length=30)),
                ('icon', models.CharField(max_length=30)),
            ],
        ),
    ]
