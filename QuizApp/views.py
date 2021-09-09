from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import AnonymousUser
# Create your views here.

def home(request):
    if request.user == AnonymousUser():
        return HttpResponse("Please Login First")
    return HttpResponse(f"<h1>{request.user.username}<h1>")