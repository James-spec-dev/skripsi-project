# Generated by Django 3.2.16 on 2023-01-26 13:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tiket', '0015_auto_20230125_1921'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movestate',
            name='user_move',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
