# Generated by Django 5.0.1 on 2024-02-02 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_rename_first_name_employee_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='phone',
            field=models.CharField(blank=True, db_column='telefono', max_length=20, null=True),
        ),
    ]
