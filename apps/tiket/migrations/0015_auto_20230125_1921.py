# Generated by Django 3.2.16 on 2023-01-25 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tiket', '0014_auto_20230125_1920'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mahasiswa',
            name='jurusan',
            field=models.CharField(blank=True, choices=[('Informatika', 'Informatika'), ('Ilmu Komunikasi', 'Ilmu Komunikasi'), ('Tekanik', 'Tekanik'), ('Psikologi', 'Psikologi')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='mahasiswa',
            name='nim',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name='mahasiswa',
            name='no_hp',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
    ]
