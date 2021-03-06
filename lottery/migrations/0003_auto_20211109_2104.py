# Generated by Django 3.2.9 on 2021-11-10 00:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lottery', '0002_auto_20211109_2051'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='code',
            field=models.IntegerField(default=0, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='contest',
            name='numbers_drawn',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='contest',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='lottery.contest'),
        ),
    ]
