from django.db import models
from django.urls import reverse


class Group(models.Model):
    """Описывает таблицу в которую могут входить устройства"""

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
    """Описывает таблицу типов устройств"""

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
    """Описывает таблицу устройств"""

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
        verbose_name="Входит в группу",
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
        
    def get_absolute_url(self) -> str:
        "Ссылка на страницу экземпляра"
        return reverse("device", kwargs={"pk": self.pk})
        

class ScenarioType(models.Model):
    """Описывает таблицу вида сценария"""

    class Meta:
        db_table = 'scenario_type'        
               
    name = models.CharField(
        db_column='name',
        max_length=50,
        help_text="Введите вид сценария",
        verbose_name="Название вида сценария"
    ) 
    
    def __str__(self):
        return self.name
        

class Scenario(models.Model):
    """Описывает таблицу сценариев"""
    class Meta:
        db_table = 'scenarios'
        
    name = models.CharField(
        db_column='name',
        max_length=50,
        unique=True,
        help_text="Введите название сценария",
        verbose_name="Название сценария"
    )
    scenario_type = models.ForeignKey(
        to='ScenarioType',
        db_column='scenario_type_id',
        on_delete=models.CASCADE,
        help_text="Укажите вид сценаярия",
        verbose_name="Вид сценария",
        null=True,        
    )
    devices = models.ManyToManyField(to='Device')
    
    def get_absolute_url(self) -> str:
        "Ссылка на страницу экземпляра"
        return reverse("scenario", kwargs={"pk": self.pk})
        
    def __str__(self):
        return self.name        
