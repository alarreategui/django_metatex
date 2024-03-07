# Generated by Django 5.0.1 on 2024-02-06 14:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kanban', '0004_fabricbatch_state_alter_processmachinery_table'),
        ('tareo', '0004_parameter_alter_behavioralevaluation_score_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ParameterProcess',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(db_column='codigo', max_length=50)),
                ('value', models.FloatField(db_column='valor')),
                ('state', models.CharField(db_column='estado', max_length=50)),
                ('parameter', models.ForeignKey(db_column='parametro', on_delete=django.db.models.deletion.CASCADE, to='tareo.parameter')),
                ('process', models.ManyToManyField(db_column='proceso', related_name='parameters', to='kanban.process')),
            ],
            options={
                'db_table': 'parametro_proceso',
            },
        ),
        migrations.CreateModel(
            name='ParameterStart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(db_column='codigo', max_length=50)),
                ('value', models.FloatField(db_column='valor')),
                ('parameter', models.ForeignKey(db_column='parametro', on_delete=django.db.models.deletion.CASCADE, to='tareo.parameter')),
                ('selected_route', models.ForeignKey(db_column='trayecto_seleccionado', on_delete=django.db.models.deletion.CASCADE, to='kanban.selectedpath')),
            ],
            options={
                'db_table': 'parametro_partida',
            },
        ),
    ]