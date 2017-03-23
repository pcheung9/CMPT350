from django.shortcuts import render, render_to_response, get_object_or_404
import requests


# Create your views here.
from django.http import HttpResponse
from explore.models import MovieObj
from django.template.response import TemplateResponse
from django.core import serializers
from itertools import chain
from explore.algorithm import *
from django.utils.safestring import mark_safe
from django.template import RequestContext
from titlecase import titlecase

def load(request):
    data = {}
    data = MovieObj.objects.all()
    json_data = serializers.serialize('json', data)
    print("Test console output")
    return HttpResponse(json_data, content_type="application/json")

def test(request):
    return TemplateResponse(request, 'cloudResults.html')


def search(request):
    titles = getTitles()
    print(titles)
    return TemplateResponse(request, 'search.html', {'titles':titles})

def results(request):
    name = request.GET['search']
    IDs = stringBuilder(name)
    results = related(15, IDs, 1, 1, 1, 1, 1)
    
    return response(request, results)

def weight(request):
    name = request.GET['update']
    print(name)
    weightArgs = name.split(",")
    name = weightArgs[0]
    
    #convert to int
    for i in range(1,6):
        weightArgs[i] = int(weightArgs[i])/50
        print(weightArgs[i])
    
    #ex
    #shrek,50,50,69,88,74,88
    #A,R,G,D,Y,S
    #1,2,3,4,5,6
    
    IDs = stringBuilder(name)
    results = related(15, IDs, weightArgs[1], weightArgs[3], weightArgs[4], weightArgs[5], weightArgs[6])
    #placeholder for rating right now
    #actorWeight, RATING PLACEHOLDER, genreWeight, directorWeight, yearWeight, scoreWeight (args)    
    
    return response(request, results)
   
def response(request, results):

    pairs = []
    
    resultsList = results.split()
    
    for pair in resultsList:
        movie = MovieObj()
        split = pair.split('|')
        temp = get_object_or_404(MovieObj, movieID=str(split[0]))
        temp.relevance = split[1]
        response = requests.post(str("http://www.omdbapi.com/?i=" + split[0])) #OMDB API call
        while response.status_code != 200:
            response = requests.post(str("http://www.omdbapi.com/?i=" + split[0]))  # OMDB API call
        print(str(split[0] + str(response)))
    
        temp.poster = response.json()["Poster"]
        temp.plot = response.json()["Plot"]
        temp.runtime = response.json()["Runtime"]
        pairs.append(temp)
    
    print(pairs)
    object_list = list(pairs)
    nonetype_querySet = MovieObj.objects.none()
    
    data = list(chain(nonetype_querySet, object_list))

    for obj in data:
        obj.title = titlecase(obj.title)
        obj.title.replace(" ,", "")

    data = serializers.serialize('json', data)
    
    #return HttpResponse(dump, mimetype='application/json')
    #return TemplateResponse(request, 'treeResults.html', ({"data": data}))
    return render_to_response("cloudResults.html", {'data':mark_safe(data)}, RequestContext(request))
