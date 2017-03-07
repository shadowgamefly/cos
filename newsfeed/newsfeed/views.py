from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
import urllib.request, json,urllib.error

def followedUser(user_id):
    followedUser = ["zyjhv", "kjfvc", "e552c"]
    return followedUser

def follewedProject(user_id):
    followedProject = ["taakn", "ah8vz", "3mp7e"]
    return followedProject

def followedTags(request):
    followedTags = ["Attention", "ERP"]
    return followedTags

def projectInTag(tag):
    pass

# def userFeed(request, user_id):
#     followedTags = followedTags(user_id)
#     followedUsers = followedUsers(user_id)
#     followedProject = followedProject(user_id)

def index(request):
    # template = loader.get_template('layout.html')
    return render(request, "layout.html")

# def bad_request(request):
#     return HttpResponse("404 error not implemented")
#
# def internal_error(request):
#     return HttpResponse("500 error not implemented")
