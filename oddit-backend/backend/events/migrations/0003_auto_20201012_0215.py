# Generated by Django 3.1.2 on 2020-10-12 02:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20201012_0210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_name',
            field=models.CharField(default='New Event', max_length=30),
        ),
    ]
