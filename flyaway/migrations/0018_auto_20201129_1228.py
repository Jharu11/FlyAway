# Generated by Django 3.1.3 on 2020-11-29 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flyaway', '0017_auto_20201129_1145'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schedule',
            name='id',
        ),
        migrations.AddField(
            model_name='schedule',
            name='ScheduleId',
            field=models.IntegerField(primary_key=True, serialize=False),
            preserve_default=False,
        ),
    ]
