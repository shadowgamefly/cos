from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import urllib.request, json


def bad_request(request):
    return HttpResponse("404 error not implemented")

def internal_error(request):
    return HttpResponse("500 error not implemented")

def index(request):
    return HttpResponse("Welcome to my playground")
