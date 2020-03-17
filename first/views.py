from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None :
            auth.login(request,user)
            return render(request,'timeline.html')
        else:
            messages.info(request,'invalid credentials')
            return redirect('login')

    else:
        return render(request,'login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
    
        if password1==password2:
            if User.objects.filter(username=username).exists() :
                messages.info(request,'Username taken')
                redirect('register')
            else:
                user = User.objects.create_user(username=username, password=password1, email =email)
                user.save()
                print('user created')
                return render(request,'timeline.html')

        else:
            messages.info(request,'password does not match')
            return redirect('register')
    
        return redirect('/')
    else:
        return render(request,'register.html')

def logout(request):
    auth.logout(request)
    return redirect('/')

