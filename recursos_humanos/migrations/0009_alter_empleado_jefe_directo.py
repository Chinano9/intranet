# Generated by Django 4.2.3 on 2023-08-16 15:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recursos_humanos', '0008_puesto_alter_empleado_foto_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empleado',
            name='jefe_directo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='recursos_humanos.empleado'),
        ),
    ]
