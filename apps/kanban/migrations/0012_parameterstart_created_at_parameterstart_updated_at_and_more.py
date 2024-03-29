# Generated by Django 5.0.1 on 2024-02-15 15:03

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kanban', '0011_qualityfield_process_code'),
        ('tareo', '0008_machineparameter_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='parameterstart',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, db_column='creacion', default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='parameterstart',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, db_column='modificacion'),
        ),
        migrations.CreateModel(
            name='ParameterFabricProcess',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(db_column='codigo', max_length=50)),
                ('value', models.FloatField(db_column='valor')),
                ('state', models.CharField(db_column='estado', max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_column='creacion')),
                ('updated_at', models.DateTimeField(auto_now=True, db_column='modificacion')),
                ('machinery_process_code', models.ManyToManyField(db_column='proceso_maquinaria_codigo', related_name='parameters', to='kanban.processmachinery')),
                ('parameter', models.ForeignKey(db_column='parametro', on_delete=django.db.models.deletion.CASCADE, to='tareo.parameter')),
            ],
            options={
                'db_table': 'parametro_tela_proceso_maquina',
            },
        ),
        migrations.DeleteModel(
            name='ParameterProcess',
        ),
    ]
