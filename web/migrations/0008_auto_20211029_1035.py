# Generated by Django 3.2.8 on 2021-10-29 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0007_auto_20211029_1029'),
    ]

    operations = [
        migrations.AddField(
            model_name='refbooking',
            name='transactionId',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='refbooking',
            name='pnr',
            field=models.CharField(max_length=50),
        ),
    ]
