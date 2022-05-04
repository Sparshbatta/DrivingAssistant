from django.db import models
from django.contrib.auth.models import User

class UserAccount(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phone = models.CharField(max_length=12,null=True, default="")
    city= models.CharField(max_length=30,null=True, default="")
    state= models.CharField(max_length=30,null=True, default="")
    address= models.CharField(max_length=400,null=True,default="")
    country = models.CharField(max_length=50,null=True, default="")
    age = models.IntegerField(null=True,default=0)
    pin = models.CharField(max_length=8,null=True,default="")
    relative_email = models.CharField(max_length=15,null=True,default="")
    relative_email_second = models.CharField(max_length=15,null=True,default="")
    profilePic = models.FileField(upload_to='accounts',default='anonymous.png')

    def __str__(self):
        return self.user.username


class WeatherStat(models.Model):
    user = models.ForeignKey(UserAccount,on_delete=models.CASCADE)
    main_stat = models.CharField(max_length=200,null=True,blank=True)
    weather_desc = models.CharField(max_length=200,null=True,blank=True)
    visibility = models.IntegerField(null=True,blank=True)
    temperature = models.DecimalField(max_digits=8,decimal_places=3,null=True,blank=True)
    pressure = models.IntegerField(null=True,blank=True)
    cloud_density = models.IntegerField(null=True,blank=True)
    wind_speed = models.DecimalField(null=True,blank=True,max_digits=8,decimal_places=3)
    time_noted = models.DateTimeField(null=True,blank=True)

    def __str__(self):
        return (self.main_stat + '->' + str(self.time_noted))  



