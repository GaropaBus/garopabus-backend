# Generated by Django 5.1.3 on 2024-11-23 00:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transporte', '0005_rename_bairro_destido_rota_bairro_destino'),
    ]

    operations = [
        migrations.AlterField(
            model_name='horarioonibus',
            name='hora_chegada',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='horarioonibus',
            name='hora_partida',
            field=models.TimeField(),
        ),
    ]
