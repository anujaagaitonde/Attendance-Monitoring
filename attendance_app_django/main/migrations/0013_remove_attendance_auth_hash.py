# Generated by Django 3.0.6 on 2020-05-21 11:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_auto_20200520_1231'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendance',
            name='auth_hash',
        ),
    ]
