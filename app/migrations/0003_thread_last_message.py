# Generated by Django 3.2.6 on 2022-01-21 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='thread',
            name='last_message',
            field=models.CharField(default='', max_length=200),
        ),
    ]
