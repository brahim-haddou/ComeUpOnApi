# Generated by Django 3.1.4 on 2020-12-29 01:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('event', '0002_auto_20201229_0155'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, unique=True)),
                ('birthday', models.DateField()),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='event.place')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='event',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner', to='event.profile'),
        ),
        migrations.AlterField(
            model_name='follower',
            name='following_user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followers', to='event.profile'),
        ),
        migrations.AlterField(
            model_name='follower',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following', to='event.profile'),
        ),
        migrations.AlterField(
            model_name='message',
            name='user_Message_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='event.profile'),
        ),
        migrations.AlterField(
            model_name='participant',
            name='user_participant_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='event.profile'),
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
