# Generated by Django 3.2.16 on 2023-01-25 02:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tiket', '0009_alter_tiketmodel_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tiketmodel',
            options={'permissions': (('manage_tiket', 'Can Manage Tiket'), ('close_tiket', 'Can Closed Tiket'))},
        ),
    ]
