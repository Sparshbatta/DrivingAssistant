from django.urls import path
from . import views


urlpatterns = [
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('trace/<int:user_id>/',views.trace,name='trace'),
    path('weather_prediction/<int:user_id>/',views.weather_prediction,name='weather_prediction'),
    path('speed_limit/<int:user_id>/',views.speed_limit,name='speed_limit'),
    path('play_music/<int:user_id>/',views.index,name='play_music'),
    path('predict_safe_drive/<int:user_id>/',views.safe_drive_predict,name='safe_drive_predict')
]
