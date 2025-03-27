from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

# Create your views here.
class SubmittableLoginView(LoginView):
    template_name = 'form.html'



def user_logout(request):
    logout(request)
    return redirect(request.META.get('HTTP_REFERER', '/')) # zostane na stránke