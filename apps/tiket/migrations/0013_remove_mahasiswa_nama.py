# Generated by Django 3.2.16 on 2023-01-25 12:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tiket', '0012_auto_20230125_1851'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mahasiswa',
            name='nama',
        ),
    ]
