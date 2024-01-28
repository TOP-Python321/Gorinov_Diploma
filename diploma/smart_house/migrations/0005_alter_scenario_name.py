# Generated by Django 4.2.7 on 2024-01-14 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smart_house', '0004_remove_scenario_air_temperature_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scenario',
            name='name',
            field=models.CharField(db_column='name', help_text='Введите название сценария', max_length=50, unique=True, verbose_name='Название сценария'),
        ),
    ]
