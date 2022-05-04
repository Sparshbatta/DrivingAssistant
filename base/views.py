from django.shortcuts import render,redirect

def home(request):
    return render(request,'index.html')

def features(request):
    if not request.user.is_authenticated:
        return redirect('/users/login/')
    return render(request,'info.html')