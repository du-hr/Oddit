# Generated by Django 3.1.2 on 2020-10-16 22:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='user_type',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Treasurer'), (2, 'President')], null=True),
        ),
    ]