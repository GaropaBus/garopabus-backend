# Generated by Django 5.1.3 on 2024-11-22 22:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transporte', '0002_remove_log_id_administrador_log_usuario_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Log',
        ),
    ]
