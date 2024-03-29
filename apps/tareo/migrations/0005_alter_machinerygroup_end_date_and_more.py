# Generated by Django 5.0.1 on 2024-02-06 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tareo', '0004_parameter_alter_behavioralevaluation_score_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='machinerygroup',
            name='end_date',
            field=models.DateTimeField(db_column='fecha_fin'),
        ),
        migrations.AlterField(
            model_name='machinerygroup',
            name='start_date',
            field=models.DateTimeField(db_column='fecha_inicio'),
        ),
        migrations.AlterField(
            model_name='worklog',
            name='end_date',
            field=models.DateTimeField(db_column='fecha_fin'),
        ),
        migrations.AlterField(
            model_name='worklog',
            name='start_date',
            field=models.DateTimeField(db_column='fecha_inicio'),
        ),
    ]
