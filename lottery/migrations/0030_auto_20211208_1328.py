# Generated by Django 3.2.9 on 2021-12-08 16:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lottery', '0029_auto_20211202_1741'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bet',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('no_prize', 'No Prize'), ('with_prize', 'With Prize')], default='pending', max_length=50),
        ),
        migrations.AlterField(
            model_name='contest',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('finished', 'Finished')], default='pending', max_length=50),
        ),
        migrations.AlterField(
            model_name='request',
            name='status',
            field=models.CharField(choices=[('open', 'Open'), ('paid', 'Paid'), ('canceled', 'Canceled'), ('finished', 'Finished')], default='open', max_length=50),
        ),
        migrations.AlterField(
            model_name='request',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='userrequest', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='status',
            field=models.CharField(default='open', max_length=50),
        ),
        migrations.AlterField(
            model_name='userprize',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
