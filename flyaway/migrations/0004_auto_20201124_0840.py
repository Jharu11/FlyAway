# Generated by Django 3.1.3 on 2020-11-24 02:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('flyaway', '0003_auto_20201124_0830'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookings',
            name='PrimaryUser',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
