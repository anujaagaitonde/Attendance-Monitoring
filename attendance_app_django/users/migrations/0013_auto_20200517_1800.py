# Generated by Django 3.0.6 on 2020-05-17 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_admin_staff'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='staff',
            options={'verbose_name_plural': 'Staff'},
        ),
        migrations.AlterField(
            model_name='student',
            name='cid',
            field=models.AutoField(max_length=8, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='student',
            name='course',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='student',
            name='year',
            field=models.IntegerField(blank=True),
        ),
    ]
