# Generated by Django 5.0.1 on 2024-02-14 20:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kanban', '0010_alter_fabricroll_kilograms_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='qualityfield',
            name='process_code',
            field=models.ForeignKey(blank=True, db_column='proceso_codigo', null=True, on_delete=django.db.models.deletion.CASCADE, to='kanban.process'),
        ),
    ]
