# Generated by Django 4.2.7 on 2023-12-22 21:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_column='name', help_text='Введите название датчика', max_length=50, verbose_name='Название датчика')),
                ('address', models.CharField(db_column='address', help_text='Введите ieee адрес датчика', max_length=50, verbose_name='ieee адрес датчика')),
            ],
            options={
                'db_table': 'devices',
            },
        ),
        migrations.CreateModel(
            name='DeviceType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_column='name', help_text='Введите тип устройства', max_length=50, verbose_name='Название типа устройства')),
                ('image', models.ImageField(help_text='Введите изображение устройства', upload_to='images', verbose_name='Изображение устройства')),
            ],
            options={
                'db_table': 'devices_type',
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_column='name', help_text='Введите название группы', max_length=50, verbose_name='Название группы')),
            ],
            options={
                'db_table': 'groups',
            },
        ),
        migrations.CreateModel(
            name='Scenario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_column='name', help_text='Введите название сценария', max_length=50, verbose_name='Сценарий')),
                ('water_temperature', models.PositiveSmallIntegerField(db_column='water_temperature', help_text='Введите температуру нагрева воды', null=True, verbose_name='Температура воды')),
                ('air_temperature', models.PositiveSmallIntegerField(db_column='air_temperature', help_text='Введите температуру воздуха', null=True, verbose_name='Температура воздуха')),
                ('max_bar', models.PositiveSmallIntegerField(db_column='max_bar', help_text='Введите значение давления при котором выключится устройство', null=True, verbose_name='Температура воздуха')),
                ('min_bar', models.PositiveSmallIntegerField(db_column='min_bar', help_text='Введите значение давления при котором включится устройство', null=True, verbose_name='Температура воздуха')),
                ('air_temperature_sensor', models.ForeignKey(db_column='air_temperature_sensor_id', help_text='Выберите датчик температуры воздуха', null=True, on_delete=django.db.models.deletion.CASCADE, to='smart_house.device', verbose_name='Датчик температуры воздуха')),
                ('socket_220', models.OneToOneField(db_column='socket_220_id', help_text='Выберите розетку', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='scenarios_as_socket_220', to='smart_house.device', verbose_name='Розетка')),
                ('water_leak_sensor_sensor', models.OneToOneField(db_column='water_leak_sensor_id', help_text='Выберите датчик протечки воды', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='scenarios_as_water_leak_sensor_sensor', to='smart_house.device', verbose_name='Датчик протечки воды')),
                ('water_pressure_sensor', models.OneToOneField(db_column='water_pressure_sensor_id', help_text='Выберите датчик давления воды', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='scenarios_as_water_pressure_sensor', to='smart_house.device', verbose_name='Датчик давления воды')),
                ('water_temperature_sensor', models.OneToOneField(db_column='water_temperature_sensor_id', help_text='Выберите датчик температуры воды', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='scenarios_as_water_temperature_sensor', to='smart_house.device', verbose_name='Датчик температуры воды')),
            ],
            options={
                'db_table': 'scenarios',
            },
        ),
        migrations.AddField(
            model_name='device',
            name='devices_type',
            field=models.ForeignKey(db_column='devices_type_id', help_text='Укажите тип устройства', null=True, on_delete=django.db.models.deletion.CASCADE, to='smart_house.devicetype', verbose_name='Тип устройства'),
        ),
        migrations.AddField(
            model_name='device',
            name='groups_id',
            field=models.ForeignKey(db_column='groups_id', help_text='Укажите в какую группу входит устройство', null=True, on_delete=django.db.models.deletion.CASCADE, to='smart_house.group', verbose_name='В какую группу входит устройство'),
        ),
    ]
