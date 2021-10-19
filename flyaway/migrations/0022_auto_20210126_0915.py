# Generated by Django 3.1.3 on 2021-01-26 03:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('flyaway', '0021_auto_20210112_1902'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookings',
            name='PNR',
        ),
        migrations.RemoveField(
            model_name='bookings',
            name='bookingStatus',
        ),
        migrations.RemoveField(
            model_name='bookings',
            name='transactionId',
        ),
        migrations.RemoveField(
            model_name='bookings',
            name='uniquenumber',
        ),
        migrations.AlterField(
            model_name='customer',
            name='name',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='refrenceBooking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_id', models.CharField(max_length=50)),
                ('flight_from', models.CharField(max_length=50)),
                ('flight_date', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flyaway.schedule')),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
