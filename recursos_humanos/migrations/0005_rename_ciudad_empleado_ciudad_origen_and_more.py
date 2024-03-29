# Generated by Django 4.2.3 on 2023-08-10 18:11

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('recursos_humanos', '0004_rename_sueldo_hora_empleado_sueldo_dia'),
    ]

    operations = [
        migrations.RenameField(
            model_name='empleado',
            old_name='ciudad',
            new_name='ciudad_origen',
        ),
        migrations.RenameField(
            model_name='empleado',
            old_name='estado',
            new_name='ciudad_residencia',
        ),
        migrations.AddField(
            model_name='empleado',
            name='estado_civil',
            field=models.CharField(blank=True, max_length=40),
        ),
        migrations.AddField(
            model_name='empleado',
            name='estado_origen',
            field=models.CharField(default=django.utils.timezone.now, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='empleado',
            name='estado_residencia',
            field=models.CharField(default='Chihuahua', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='empleado',
            name='jefe_directo',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='empleado',
            name='num_casa',
            field=models.CharField(default=0, max_length=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='empleado',
            name='tel_casa',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
