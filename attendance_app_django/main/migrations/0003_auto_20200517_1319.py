# Generated by Django 3.0.6 on 2020-05-17 13:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20200517_1207'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'permissions': [('can_lead', 'User can lead event'), ('can_attend', 'User can attend event')]},
        ),
    ]
