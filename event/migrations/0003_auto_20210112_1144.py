# Generated by Django 3.1.4 on 2021-01-12 10:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0002_auto_20210109_1545'),
    ]

    operations = [
        migrations.RenameField(
            model_name='follower',
            old_name='followers',
            new_name='follow',
        ),
    ]
