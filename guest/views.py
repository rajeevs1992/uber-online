from guest.forms import LoginForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from ride.models import Request

def welcome(request):
    if request.user.is_authenticated():
        return redirect('request')
    if request.method == 'GET':
        return render(request, 'welcome.html', {'form' : LoginForm()})
    else:
        form = LoginForm(request.POST)
        if not form.is_valid():
            return render(request, 'welcome.html', {'form' : form})
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)

        if user is not None and user.is_active:
            login(request, user)
            return redirect('request')
        else:
            form.add_error('username', 'Username and password do not match')
            return render(request, 'welcome.html', {'form' : form})

def user_logout(request):
    if request.user is not None and request.user.is_authenticated():
        Request.objects.filter(user=request.user).delete()
        logout(request)
    return redirect('welcome')
