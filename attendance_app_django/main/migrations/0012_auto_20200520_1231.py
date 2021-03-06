# Generated by Django 3.0.6 on 2020-05-20 12:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_auto_20200517_1804'),
        ('main', '0011_attendance_auth_hash'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendance',
            name='authenticated',
        ),
        migrations.AlterField(
            model_name='attendance',
            name='auth_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.CreateModel(
            name='Verification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('verified', models.BooleanField(default=False)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_to_verify', to='main.Event')),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Staff')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Event')),
            ],
        ),
    ]
