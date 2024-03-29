# Generated by Django 4.2.3 on 2023-08-14 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recursos_humanos', '0005_rename_ciudad_empleado_ciudad_origen_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='empleado',
            name='foto_url',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='empleado',
            name='ciudad_origen',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='empleado',
            name='estado_origen',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
