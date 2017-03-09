from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
import urllib.request, json , urllib.error
from collections import Counter
import operator
import copy

def userProjectsFind(userid): #give name, projects,
    url = "https://api.osf.io/v2/users/" + userid
    url_nodes = url + "/nodes" + "?format=json";
    response_node = urllib.request.urlopen(url_nodes)
    data = json.loads(response_node.read().decode('utf-8'))
    projects = []
    for i in range(len(data['data'])):
        projects.append(data['data'][i]['id'])
    p = {}
    for pro in projects :
        p[pro] = 50
    return Counter(p)

def numProjects(userid): #give name, projects,
    url = "https://api.osf.io/v2/users/" + userid + "/nodes/?filter%5Bparent%5D=null" + "&format=json"
    response = urllib.request.urlopen(url)
    data = json.loads(response.read().decode('utf-8'))
    projects = []
    num = data['links']['meta']['total']
    return num

def searchTag(tag):
    project_titles = []
    project_ids = []
    url = 'https://api.osf.io/v2/search/?q=tags:(' + tag + ")&format=json"
    response_search = urllib.request.urlopen(url)
    data = json.loads(response_search.read().decode('utf-8'))
    for i in range(len(data['data'])):
        try :
            project_ids.append(data['data'][i]['id'])
        except TypeError:
            continue
    p = {}
    for pro in project_ids :
        p[pro] = 10
    return Counter(p)

def followedUser(user_id):
    followedUser = ["pf5vs", "hsey5", "wnsja"]
    return followedUser

def followedProject(user_id):
    followedProject = ["taakn" , "3mp7e", "tazyx"]
    return set(followedProject)

def followedTags(user_id):
    followedTags = ["psychology", "education"]
    return followedTags

def retrieveProjectInfo(project_id):
    url = "https://api.osf.io/v2/nodes/" + project_id + "?format=json"
    response_node = urllib.request.urlopen(url)
    data = json.loads(response_node.read().decode('utf-8'))
    data = data["data"]["attributes"]
    data["id"] = project_id
    return data

def retrieveUserInfo(user_id):
    url = "https://api.osf.io/v2/users/" + user_id + "/?format=json"
    response_node = urllib.request.urlopen(url)
    data = json.loads(response_node.read().decode('utf-8'))
    photo = data["data"]["links"]["profile_image"]
    data = data["data"]["attributes"]
    data["id"] = user_id
    data["photo"] = photo
    return data

def projToUser(projid):
    url = 'https://api.osf.io/v2/nodes/' + projid + "/contributors/?format=json"
    contributors = []
    response = urllib.request.urlopen(url)
    data = json.loads(response.read().decode('utf-8'))
    for i in range(len(data['data'])):
        try :
            userId = data['data'][i]['embeds']['users']['data']['id']
            contributors.append(userId)
        except TypeError:
            continue
    return contributors[0]


def index(request):
    return render(request, "layout.html")

def userFeed(request):
    user_id = "abc"
    Tags = followedTags(user_id)
    tagProjects = Counter({})
    # append all tag related projects in tagProject
    for tag in Tags :
        tagProjects = tagProjects + searchTag(tag)
    # append all user related projects
    users = followedUser(user_id)
    userPro = Counter({})
    for user in users:
        userPro = userPro + userProjectsFind(user)
    # add them together
    l = userPro + tagProjects

    # get followed projects
    followed = followedProject(user_id)

    # remove all already followed projects in the feed
    keyList = []
    for key in l.keys() :
        keyList.append(key)
    for k in keyList :
        if k in followed:
            del l[k]

    # sort all data by their relevance score
    sorted_l = sorted(l.items(), key=operator.itemgetter(1))[::-1]

    # remove relavance score
    sorted_l = [key[0] for key in sorted_l]

    # retrieve relavant data
    projectList = []
    counter = 0
    for project in sorted_l:
        # if project in tagProject.keys():
        try :
            projectInfo = retrieveProjectInfo(project)
        except urllib.request.HTTPError:
            continue

        if projectInfo["id"] in tagProjects.keys() :
            projectInfo["base"] = "tag"
        else :
            projectInfo["base"] = "user"

        if (projectInfo["description"] is  None ) or projectInfo["description"] == "":
            del projectInfo["description"]
        projectInfo["date_created"] = projectInfo["date_created"][:10]
        projectList.append(projectInfo)
        counter += 1

    userList = []
    for i in range(2):
        project = sorted_l[i]
        user = projToUser(project)
        userInfo = retrieveUserInfo(user)
        # userProjects = numProjects(users[i])
        # userInfo["numofProjects"] = userProjects
        userInfo["numProjects"] = numProjects(user)

        userInfo["date_registered"] = userInfo["date_registered"][:10]
        userList.append(userInfo)

    return render(request, 'userfeed.html', {'projects': projectList, 'users': userList})

def userFollow(request):
    user_id = "abcde"
    projects = followedProject(user_id)
    projectList=[]
    for project in projects:
        projectInfo = retrieveProjectInfo(project)

        projectInfo["date_created"] = projectInfo["date_created"][:10]

        projectList.append(projectInfo)

    users = followedUser(user_id)
    userList=[]
    for i in range(2):
        userInfo = retrieveUserInfo(users[i])
        # userProjects = numProjects(users[i])
        userInfo["numProjects"] = numProjects(users[i])
        userInfo["date_registered"] = userInfo["date_registered"][:10]
        userList.append(userInfo)

    return render(request, 'follow.html', {'projects': projectList, 'users': userList})

def load_page(request):
    return render(request, 'load_page.html')


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

# def bad_request(request):
#     return HttpResponse("404 error not implemented")
#
# def internal_error(request):
#     return HttpResponse("500 error not implemented")
