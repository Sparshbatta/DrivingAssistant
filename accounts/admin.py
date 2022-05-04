from django.contrib import admin
from .models import UserAccount, WeatherStat

admin.site.register(UserAccount)
admin.site.register(WeatherStat)