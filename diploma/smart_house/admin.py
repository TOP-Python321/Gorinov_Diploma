from django.contrib import admin


from .models import Group, DeviceType, Device, Scenario, ScenarioType

admin.site.register(Group)
admin.site.register(DeviceType)
admin.site.register(Device)
admin.site.register(Scenario)
admin.site.register(ScenarioType)
