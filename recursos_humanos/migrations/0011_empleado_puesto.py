# Generated by Django 4.2.3 on 2023-08-18 14:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recursos_humanos', '0010_remove_empleado_puesto'),
    ]

    operations = [
        migrations.AddField(
            model_name='empleado',
            name='puesto',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='recursos_humanos.puesto'),
            preserve_default=False,
        ),
    ]