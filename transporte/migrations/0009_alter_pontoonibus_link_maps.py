# Generated by Django 5.1.3 on 2024-12-14 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transporte', '0008_rota_id_rota_principal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pontoonibus',
            name='link_maps',
            field=models.TextField(blank=True, null=True),
        ),
    ]
