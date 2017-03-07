from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
import urllib.request, json,urllib.error
#
# def followedUser(request):
#     user_id = requst.kwargs["userid"]
#
#
#     followedUser = ["zyjhv", "kjfvc", "e552c"]
#     return followedUser
#
# def follewedProject(request):
#     user_id
#
#     followedProject = ["taakn", "ah8vz", "3mp7e"]
#     return followedProject
#
# def followedTags(request):
#     followedTags = ["Attention", "ERP"]
#     return followedTags
#
# def projectInTag(tag):
#     tag = ["ERP"]
#     {"id" : "abcde", "Title" : "abcdefg", "collabrator" : ["Jerry", "Jacob", "sarah"]}
#     return correspondingProjects = [[]]

def userFeed(request, user_id):
    requester = urllib.request.Request("https://api.osf.io/v2/users/" + user_id)
    try:
        response = urllib.request.urlopen(requester).read().decode('utf-8')
    except urllib.error.HTTPError as err:
        if err.code == 404:
            return HttpResponse("Not Found")
    read = json.loads(response)
    return JsonResponse({"name" : read['data']['attributes']['full_name'], "related projects" : ["abcdef", "asdasd"]})

def index(request):
    return HttpResponse("Welcome to my playground")

# def bad_request(request):
#     return HttpResponse("404 error not implemented")
#
# def internal_error(request):
#     return HttpResponse("500 error not implemented")
