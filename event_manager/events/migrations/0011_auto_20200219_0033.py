# Generated by Django 3.0.3 on 2020-02-19 00:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0010_auto_20200219_0031'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='registration',
            unique_together={('event', 'email')},
        ),
    ]
