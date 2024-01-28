# Generated by Django 4.2.7 on 2024-01-26 20:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('smart_house', '0005_alter_scenario_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='scenario',
            old_name='devices_id',
            new_name='devices',
        ),
        migrations.AlterField(
            model_name='device',
            name='groups_id',
            field=models.ForeignKey(blank=True, db_column='groups_id', help_text='Укажите в какую группу входит устройство', null=True, on_delete=django.db.models.deletion.CASCADE, to='smart_house.group', verbose_name='Входит в группу'),
        ),
    ]
