# Generated by Django 5.1.1 on 2024-10-26 00:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_userprofile_location'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='location',
        ),
    ]