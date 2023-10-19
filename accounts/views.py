import sys
from django.contrib import auth, messages
from django.core.mail import send_mail
from django.shortcuts import redirect
from accounts.models import Token
from django.urls import reverse
from django.contrib.auth import logout


def send_login_email(request):
    email = request.POST['email']
    token = Token.objects.create(email=email)
    url = request.build_absolute_uri(  
        reverse('login') + '?token=' + str(token.uid)
    )
    message_body = f'Use this link to log in:\n\n{url}'
    send_mail(
        'Your login link for c-learning',
         message_body,
        'noreply@c-learning',
        [email]
    )
    messages.add_message(
        request,
        messages.SUCCESS,
        "Check your email, we've sent you a link you can use to log in."
    )
    return redirect('/')

def login(request):
    user = auth.authenticate(request=request, uid=request.GET.get('token'))
    if user:
        auth.login(request, user)
    return redirect('/')

def logout(request):
    auth.logout(request)
    return redirect('/')

