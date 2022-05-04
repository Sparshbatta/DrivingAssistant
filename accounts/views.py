from time import time
from django.http import HttpResponse
from django.shortcuts import render, redirect
from numpy import Inf
from .models import UserAccount, WeatherStat
from django.contrib.auth.models import User
from django.contrib import auth
from decimal import Decimal
import requests
import pandas as pd
import math
from dateutil import parser
import json 
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix
x = None
# Create your views here.
def index(request,user_id):
    ar = 'https://open.spotify.com/artist/3tSmEw5WMGAZ6sxt9Dt3Nt?si=uq_BtntFQ9-1HCLmHPGVAA'
    artist_uri='https://open.spotify.com/artist/0jgAONnsHxrwAlhkMUVS78?si=VyOEarivRzuELCkMkbltRg'
    spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id='9dae8c621c024addbd38cbd43cef8dd1',client_secret='cc35add278fc42b2b69a07be5a105c0f',))
    results = spotify.artist_top_tracks(artist_uri)
    results2=spotify.artist_top_tracks(ar)
    print(results)
    final_result=results['tracks']+results2['tracks']
    print()
    print(final_result)
    return render(request,'spot.html',{"results":final_result})
  


def register(request):
    if request.method=='POST':
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        age = request.POST.get('age')
        address = request.POST.get('address')
        state = request.POST.get('state')
        city = request.POST.get('city')
        country = request.POST.get('country')
        pin = request.POST.get('pin')
        file = request.FILES['image']
        print(file)
        user = User.objects.create_user(username=username,first_name=first_name,last_name=last_name,email=email,password=password)
        finalUser = UserAccount.objects.create(user=user,age=age,address=address,phone=phone,state=state,city=city,country=country,pin=pin,profilePic=file)
        finalUser.save()
        return redirect('/')
    else:
        return render(request,"accounts/register.html",{})
    

def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            return HttpResponse('Invalid Credentials')
    else:
        return render(request,'accounts/login.html',{})


def logout(request):
    auth.logout(request)
    return redirect('/')

def currLocationStats(user_id):
    currUser = UserAccount.objects.get(user_id=user_id)
    city = str(currUser.address)
    print(city)
    parameters = {
        "key" : "XMSMT4Y38dET1KnpPwcHfG1fQi2CwOz8",
        "location": city
    }
    locResponse = requests.get('http://www.mapquestapi.com/geocoding/v1/address',params=parameters)
    jsonData = json.loads(locResponse.text)['results']
    lat = jsonData[0]['locations'][0]['latLng']['lat']
    long = jsonData[0]['locations'][0]['latLng']['lng']
    return [lat,long,currUser,city]


def trace(request,user_id):
    [lat,long,currUser,city]=currLocationStats(user_id)
    params = {'currUser':currUser,'latitude':lat,'longitude':long,'city':city}
    return render(request,"accounts/trace.html",params)


def weather_prediction(request,user_id):
    [lat,long,currUser,city]=currLocationStats(user_id)
    api_key = 'ddbadb761977f7530d07fccc631e3aef'
    URL = 'https://api.openweathermap.org/data/2.5/forecast?lat='+str(lat)+'&lon='+str(long)+'&appid='+api_key
    response = requests.get(URL)
    print(URL)
    if response.status_code == 200:
        if len(WeatherStat.objects.filter(user=currUser)):
            WeatherStat.objects.filter(user=currUser).delete()

        data = response.json()
        for i in data['list']:
            temperature = Decimal(i['main'].get('temp'))
            pressure = int(i['main'].get('pressure'))
            weather_desc = i['weather'][0].get('description')
            main_stat = i['weather'][0].get('main')
            visibility = int(i['visibility'])
            cloud_density = int(i['clouds'].get('all'))
            wind_speed = Decimal(int(i['wind'].get('speed')))
            time_noted = parser.parse(i['dt_txt'])
            WeatherStat.objects.create(user=currUser, temperature=temperature, pressure=pressure, visibility=visibility,weather_desc=weather_desc,main_stat=main_stat,cloud_density=cloud_density,wind_speed=wind_speed,time_noted=time_noted)
        
        weather_stat_queryset = WeatherStat.objects.filter(user=currUser)
        params = {'currUser':currUser,'latitude':lat,'longitude':long,'weather_stat_queryset':weather_stat_queryset,'city':city}
        
        weatherInfo = dict()
        for i in weather_stat_queryset:
            if 'temperature' in weatherInfo:
                weatherInfo['temperature'].append(int(i.temperature))
            
            else:
                weatherInfo['temperature'] = [int(i.temperature)]

            if 'pressure' in weatherInfo:
                weatherInfo['pressure'].append(int(i.pressure))
            
            else:
                weatherInfo['pressure'] = [int(i.pressure)]

            if 'cloud_density' in weatherInfo:
                weatherInfo['cloud_density'].append(int(i.cloud_density))
            
            else: 
                weatherInfo['cloud_density'] = [int(i.cloud_density)]

            if 'visibility' in weatherInfo:
                weatherInfo['visibility'].append(int(i.visibility))
            
            else:
                weatherInfo['visibility'] = [int(i.visibility)]
            

            if 'wind_speed' in weatherInfo:
                weatherInfo['wind_speed'].append(math.ceil(float(i.wind_speed)))
            
            else: 
                weatherInfo['wind_speed'] = [math.ceil(float(i.wind_speed))]

        
        df = pd.DataFrame(weatherInfo)
        print(df.head(5))

        return render(request,'accounts/weather_prediction.html',params)


def speed_limit(request,user_id):
    
    [lat,long,currUser,city]=currLocationStats(user_id)
    api_key = 'XoUSX3ikHzoo1GzlObfCnFvBUxHHmOjp'
    URL = 'https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json?key='+api_key+'&point='+str(lat)+','+str(long)
    print(URL)
    response = requests.get(URL)
    if response.status_code == 200:
        jsonData = response.json()
        optimalSpeed = jsonData['flowSegmentData'].get('freeFlowSpeed')
        print(optimalSpeed)
        params = {'optimalSpeed':optimalSpeed,'currUser':currUser,'city':city}
        return render(request,'accounts/speed_limit.html',params)
    else:
        return render(request,'accounts/speed_limit.html',{})
    

def safe_drive_predict(request,user_id):
    resultDict = {}
    [lat,long,currUser,city]=currLocationStats(user_id)
    api_key = 'ddbadb761977f7530d07fccc631e3aef'
    URL = 'https://api.openweathermap.org/data/2.5/forecast?lat='+str(45.90)+'&lon='+str(34.90)+'&appid='+api_key
    response = requests.get(URL)
    print(URL)
    if response.status_code == 200:
        if len(WeatherStat.objects.filter(user=currUser)):
            WeatherStat.objects.filter(user=currUser).delete()

        data = response.json()
        for i in data['list']:
            temperature = Decimal(i['main'].get('temp'))
            pressure = int(i['main'].get('pressure'))
            weather_desc = i['weather'][0].get('description')
            main_stat = i['weather'][0].get('main')
            visibility = int(i['visibility'])
            cloud_density = int(i['clouds'].get('all'))
            wind_speed = Decimal(int(i['wind'].get('speed')))
            time_noted = parser.parse(i['dt_txt'])
            WeatherStat.objects.create(user=currUser, temperature=temperature, pressure=pressure, visibility=visibility,weather_desc=weather_desc,main_stat=main_stat,cloud_density=cloud_density,wind_speed=wind_speed,time_noted=time_noted)
        
        weather_stat_queryset = WeatherStat.objects.filter(user=currUser)
        params = {'currUser':currUser,'latitude':lat,'longitude':long,'weather_stat_queryset':weather_stat_queryset,'city':city}


        #ML Section

        weatherInfo = dict()
        for i in weather_stat_queryset:
            if 'main_stat' in weatherInfo:
                weatherInfo['main_stat'].append(i.main_stat)
            
            else:
                weatherInfo['main_stat'] = [i.main_stat]

            if 'temperature' in weatherInfo:
                weatherInfo['temperature'].append(int(i.temperature))
            
            else:
                weatherInfo['temperature'] = [int(i.temperature)]

            if 'pressure' in weatherInfo:
                weatherInfo['pressure'].append(float(i.pressure))
            
            else:
                weatherInfo['pressure'] = [float(i.pressure)]

            if 'cloud_density' in weatherInfo:
                weatherInfo['cloud_density'].append(int(i.cloud_density))
            
            else:
                weatherInfo['cloud_density'] = [int(i.cloud_density)]

            if 'visibility' in weatherInfo:
                weatherInfo['visibility'].append(int(i.visibility))
            
            else:
                weatherInfo['visibility'] = [int(i.visibility)]
            

            if 'wind_speed' in weatherInfo:
                weatherInfo['wind_speed'].append(float(i.wind_speed))
            
            else:
                weatherInfo['wind_speed'] = [float(i.wind_speed)]
        df = pd.DataFrame(weatherInfo) 



        #clouds
        X = df[['pressure','wind_speed','visibility','temperature']]
        Y = df['cloud_density']
        X_train, X_test, y_train, y_test = train_test_split(X,Y,test_size=0.20)
        scaler = StandardScaler()
        scaler.fit(X_train)
        X_train = scaler.transform(X_train)
        X_test = scaler.transform(X_test)
        classifier = KNeighborsClassifier(n_neighbors=6)
        classifier.fit(X_train,y_train)
        y_pred = classifier.predict(X_test)
        finalResult = classification_report(y_test, y_pred,output_dict=True)
        df2 = pd.DataFrame(finalResult).transpose()
        dict1 = dict(df2[['support']].iloc[:-2,:].idxmax())
        resultDict['clouds']=dict1['support']


         #main stat
        X = df[['pressure','wind_speed','visibility','temperature','cloud_density']]
        Y = df['main_stat']
        X_train, X_test, y_train, y_test = train_test_split(X,Y,test_size=0.20)
        scaler = StandardScaler()
        scaler.fit(X_train)
        X_train = scaler.transform(X_train)
        X_test = scaler.transform(X_test)
        classifier = KNeighborsClassifier(n_neighbors=6)
        classifier.fit(X_train,y_train)
        y_pred = classifier.predict(X_test)
        finalResult = classification_report(y_test, y_pred,output_dict=True)
        df2 = pd.DataFrame(finalResult).transpose()
        dict1 = dict(df2[['support']].iloc[:-2,:].idxmax())
        resultDict['main_stat']=dict1['support']

         #temperature
        X = df[['pressure','wind_speed','visibility','cloud_density']]
        Y = df['temperature']
        X_train, X_test, y_train, y_test = train_test_split(X,Y,test_size=0.20)
        scaler = StandardScaler()
        scaler.fit(X_train)
        X_train = scaler.transform(X_train)
        X_test = scaler.transform(X_test)
        classifier = KNeighborsClassifier(n_neighbors=6)
        classifier.fit(X_train,y_train)
        y_pred = classifier.predict(X_test)
        finalResult = classification_report(y_test, y_pred,output_dict=True)
        df2 = pd.DataFrame(finalResult).transpose()
        dict1 = dict(df2[['support']].iloc[:-2,:].idxmax())
        resultDict['temperature']=dict1['support']

         #pressure
        X = df[['temperature','wind_speed','visibility','cloud_density']]
        Y = df['pressure']
        X_train, X_test, y_train, y_test = train_test_split(X,Y,test_size=0.20)
        scaler = StandardScaler()
        scaler.fit(X_train)
        X_train = scaler.transform(X_train)
        X_test = scaler.transform(X_test)
        classifier = KNeighborsClassifier(n_neighbors=6)
        classifier.fit(X_train,y_train)
        y_pred = classifier.predict(X_test)
        finalResult = classification_report(y_test, y_pred,output_dict=True)
        df2 = pd.DataFrame(finalResult).transpose()
        dict1 = dict(df2[['support']].iloc[:-2,:].idxmax())
        resultDict['pressure']=dict1['support']

        #wind_speed
        X = df[['temperature','pressure','visibility','cloud_density']]
        Y = df['wind_speed']
        X_train, X_test, y_train, y_test = train_test_split(X,Y,test_size=0.20)
        scaler = StandardScaler()
        scaler.fit(X_train)
        X_train = scaler.transform(X_train)
        X_test = scaler.transform(X_test)
        classifier = KNeighborsClassifier(n_neighbors=6)
        classifier.fit(X_train,y_train)
        y_pred = classifier.predict(X_test)
        finalResult = classification_report(y_test, y_pred,output_dict=True)
        df2 = pd.DataFrame(finalResult).transpose()
        dict1 = dict(df2[['support']].iloc[:-2,:].idxmax())
        resultDict['wind_speed']=dict1['support']

        #visibility
        X = df[['temperature','pressure','visibility','cloud_density']]
        Y = df['visibility']
        X_train, X_test, y_train, y_test = train_test_split(X,Y,test_size=0.20)
        scaler = StandardScaler()
        scaler.fit(X_train)
        X_train = scaler.transform(X_train)
        X_test = scaler.transform(X_test)
        classifier = KNeighborsClassifier(n_neighbors=6)
        classifier.fit(X_train,y_train)
        y_pred = classifier.predict(X_test)
        finalResult = classification_report(y_test, y_pred,output_dict=True)
        df2 = pd.DataFrame(finalResult).transpose()
        dict1 = dict(df2[['support']].iloc[:-2,:].idxmax())
        resultDict['visibility']=dict1['support']
        return render(request,"accounts/mlResults.html",resultDict)  
