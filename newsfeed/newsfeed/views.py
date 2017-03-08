from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
import urllib.request, json,urllib.error
from collections import Counter
import operator
import copy

def userProjects(userid): #give name, projects,
    url = "https://api.osf.io/v2/users/" + userid
    # url_name = url + "?format=json";
    # response_name = urllib.request.urlopen(url_name)
    # data_name = json.loads(response_name.read().decode('utf-8'))
    url_nodes = url + "/nodes" + "?format=json";
    response_node = urllib.request.urlopen(url_nodes)
    data = json.loads(response_node.read().decode('utf-8'))
    # print(data_node['data']['links']['meta']['total'])
    projects = []
    for i in range(len(data['data'])):
        projects.append(data['data'][i]['id'])
    #
    # dict = {
    # "name" : data_name['data']['attributes']['full_name'],
    # "related projects" : projects
    # }
    p = {}
    for pro in projects :
        p[pro] = 50
    return Counter(p)

def searchTag(tag):
    project_titles = []
    project_ids = []
    url = 'https://api.osf.io/v2/search/?q=tags:(' + tag + ")&format=json"
    response_search = urllib.request.urlopen(url)
    data = json.loads(response_search.read().decode('utf-8'))
    for i in range(len(data['data'])):
        try :
            project_titles.append(data['data'][i]['attributes']['title'])
            project_ids.append(data['data'][i]['id'])
        except TypeError:
            continue
    # dict = {
    # "titles" : project_titles,
    # "project_ids" : project_ids
    # }
    p = {}
    for pro in project_ids :
        p[pro] = 10
    return Counter(p)
    # return dict



def followedUser(user_id):
    followedUser = ["pf5vs", "hsey5", "wnsja"]
    return followedUser

def followedProject(user_id):
    followedProject = ["taakn" , "ah8vz", "3mp7e", "tazyx"]
    return set(followedProject)

def followedTags(user_id):
    followedTags = ["psychology", "education"]
    return followedTags

# def projectInTag(tag):
#     if tag == "psychology" :
#         projects = Counter({"eq3s2" :10, "g3fmn":10, "469us":10, "2h83z":10, "4fjwr":10, "ey65c":10})
#     elif tag == "education":
#         projects = Counter({"abcde" :10, "469us":10})
#     return projects

# def projectByUser(user_id):
#     if user_id == "pf5vs":
#         projects = Counter({"eq3s2":50, "469us":50, "abcde":50})
#     elif user_id == "hsey5":
#         projects = Counter({"ey65c":50, "469us":50, "zaiss":50})
#     else :
#         projects = Counter({"ajsga":50})
#     return projects

def userFeed(request):
    user_id = "abc"
    l = Counter({})
    Tags = followedTags(user_id)
    for tag in Tags :
        l = l + searchTag(tag)
    users = followedUser(user_id)
    for user in users:
        l = l + userProjects(user)
    l = dict(l)
    followed = followedProject(user_id)
    keyList = []
    for key in l.keys() :
        keyList.append(key)
    for k in keyList :
        if k in followed:
            del l[k]
    sorted_l = sorted(l.items(), key=operator.itemgetter(1))[::-1]
    sorted_l = [key[0] for key in sorted_l]
    infoList = []
    counter = 0
    for project in sorted_l:
        if counter > 5 :
            break
        projectInfo = retrieveProjectInfo(project)
        infoList.append(projectInfo)
        counter += 1
    return render(request, 'layout.html', {'projects': infoList})

def retrieveProjectInfo(project_id):
    url = "https://api.osf.io/v2/nodes/" + project_id + "?format=json";
    response_node = urllib.request.urlopen(url)
    data = json.loads(response_node.read().decode('utf-8'))
    data = data["data"]["attributes"]
    data["id"] = project_id
    return data

def index(request):
    # template = loader.get_template('layout.html')
    return render(request, "layout.html")

# def bad_request(request):
#     return HttpResponse("404 error not implemented")
#
# def internal_error(request):
#     return HttpResponse("500 error not implemented")
