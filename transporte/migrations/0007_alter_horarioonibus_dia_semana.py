# Generated by Django 5.1.3 on 2024-12-02 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transporte', '0006_alter_horarioonibus_hora_chegada_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='horarioonibus',
            name='dia_semana',
            field=models.CharField(choices=[('dia_util', 'Dia Util'), ('final_semana_feriado', 'Final Semana Feriado')], max_length=20),
        ),
    ]
