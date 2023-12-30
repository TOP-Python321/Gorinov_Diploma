from django.db import models


class Group(models.Model):
    class Meta:
        db_table = 'groups'
        
    name = models.CharField(
        db_column='name',
        max_length=50,
        help_text="Введите название группы",
        verbose_name="Название группы"
    )
    def __str__(self):
        return self.name
    
class DeviceType(models.Model):
    class Meta:
        db_table = 'devices_type'        
               
    name = models.CharField(
        db_column='name',
        max_length=50,
        help_text="Введите тип устройства",
        verbose_name="Название типа устройства"
    )
    image = models.ImageField(
        upload_to='images',
        help_text="Введите изображение устройства",
        verbose_name="Изображение устройства"
    )
    def __str__(self):
        return self.name

class Device(models.Model):
    class Meta:
        db_table = 'devices'
        
    name = models.CharField(
        db_column='name',
        max_length=50,
        help_text="Введите название датчика",
        verbose_name="Название датчика"
    )
    address = models.CharField(
        db_column='address',
        max_length=50,
        help_text="Введите ieee адрес датчика",
        verbose_name="ieee адрес датчика"
    )
    json_data = models.JSONField(
        db_column='json_data',
        null=True,
        blank=True
    )
    groups_id = models.ForeignKey(
        to='Group',
        db_column='groups_id',
        on_delete=models.CASCADE,
        help_text="Укажите в какую группу входит устройство",
        verbose_name="В какую группу входит устройство",
        null=True,
        blank=True
    )
    devices_type= models.ForeignKey(
        to='DeviceType',
        db_column='devices_type_id',
        on_delete=models.CASCADE,
        help_text="Укажите тип устройства",
        verbose_name="Тип устройства",
        null=True,
        blank=True
    )
    def __str__(self):
        return self.name
    
class Scenario(models.Model):
    class Meta:
        db_table = 'scenarios'
        
    name = models.CharField(
        db_column='name',
        max_length=50,
        help_text="Введите название сценария",
        verbose_name="Сценарий"
    )
    water_temperature = models.PositiveSmallIntegerField(
        db_column='water_temperature',      
        help_text="Введите температуру нагрева воды",
        verbose_name="Температура воды",
        null=True,
        blank=True
    )
    air_temperature = models.PositiveSmallIntegerField(
        db_column='air_temperature',      
        help_text="Введите температуру воздуха",
        verbose_name="Температура воздуха",
        null=True,
        blank=True
    )
    max_bar = models.PositiveSmallIntegerField(
        db_column='max_bar',      
        help_text="Введите значение давления при котором выключится устройство",
        verbose_name="Температура воздуха",
        null=True,
        blank=True
    )
    min_bar = models.PositiveSmallIntegerField(
        db_column='min_bar',      
        help_text="Введите значение давления при котором включится устройство",
        verbose_name="Температура воздуха",
        null=True,
        blank=True
    )
    water_pressure_sensor= models.OneToOneField(
        to='Device',
        db_column='water_pressure_sensor_id',
        on_delete=models.CASCADE,
        help_text="Выберите датчик давления воды",
        verbose_name="Датчик давления воды",
        related_name="scenarios_as_water_pressure_sensor",
        null=True,
        blank=True
    )
    # ПОМЕНЯТЬ НА СВЯЗЬ ОДИН КО МНОГИМ?
    water_leak_sensor_sensor= models.OneToOneField(
        to='Device',
        db_column='water_leak_sensor_id',
        on_delete=models.CASCADE,
        related_name="scenarios_as_water_leak_sensor_sensor",
        help_text="Выберите датчик протечки воды",
        verbose_name="Датчик протечки воды",
        null=True,
        blank=True
    )
    socket_220= models.OneToOneField(
        to='Device',
        db_column='socket_220_id',
        on_delete=models.CASCADE,
        related_name="scenarios_as_socket_220",
        help_text="Выберите розетку",
        verbose_name="Розетка",
        null=True,
        blank=True
    )
    water_temperature_sensor= models.OneToOneField(
        to='Device',
        db_column='water_temperature_sensor_id',
        on_delete=models.CASCADE,
        related_name="scenarios_as_water_temperature_sensor",
        help_text="Выберите датчик температуры воды",
        verbose_name="Датчик температуры воды",
        null=True,
        blank=True
    )
    air_temperature_sensor= models.ForeignKey(
        to='Device',
        db_column='air_temperature_sensor_id',
        on_delete=models.CASCADE,
        help_text="Выберите датчик температуры воздуха",
        verbose_name="Датчик температуры воздуха",
        null=True,
        blank=True
    )
    def __str__(self):
        return self.name