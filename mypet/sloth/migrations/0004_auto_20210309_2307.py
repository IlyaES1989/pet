# Generated by Django 3.1.7 on 2021-03-09 18:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sloth', '0003_report_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='variable',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='variable',
            name='month',
            field=models.PositiveSmallIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='variable',
            name='year',
            field=models.PositiveSmallIntegerField(max_length=4),
        ),
    ]