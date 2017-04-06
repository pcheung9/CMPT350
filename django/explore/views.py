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

def search(request):
    titles = getTitles()
    return TemplateResponse(request, 'search.html', {'titles': titles})

#working data
def bargraphs(request):
    movies = MovieObj.objects.all().filter(year=1993)
    #movies = MovieObj.objects.all()
    data = serializers.serialize('json', movies)
    return TemplateResponse(request, 'bargraphs.html', {'data': data})



def results(request):
    name = request.GET['search']
    print ("Selected movie", name)
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
        weightArgs[i] = int(weightArgs[i])/10
        print(weightArgs[i])

    # ex
    # shrek,50,50,69,88,74,88
    # A,R,G,D,Y,S
    # 1,2,3,4,5,6

    IDs = stringBuilder(name)
    results = related(15, IDs, weightArgs[1], weightArgs[3], weightArgs[4], weightArgs[5], weightArgs[6])
    # placeholder for rating right now
    # actorWeight, RATING PLACEHOLDER, genreWeight, directorWeight, yearWeight, scoreWeight (args)

    return response(request, results)

def details(request):
    node_ID = request.GET['node_ID']
    print(request.GET['node_ID'])
    
    pairs = []
    temp = get_object_or_404(MovieObj, movieID=str(node_ID))
    
    response = requests.post(str("http://www.omdbapi.com/?i=" + node_ID)) #OMDB API call
    while response.status_code != 200:
        response = requests.post(str("http://www.omdbapi.com/?i=" + node_ID)) #OMDB API call
    
    print(str(node_ID + str(response)))
    temp.poster = response.json()["Poster"]
    temp.plot = response.json()["Plot"]
    temp.runtime = response.json()["Runtime"]    
    
    temp.awards = response.json()["Awards"]
    temp.IMDBScore = response.json()["imdbRating"]
    temp.tomatoes = response.json()["Ratings"][1]["Value"]
    temp.metascore = response.json()["Metascore"]
    temp.production = response.json()["Production"]
    temp.boxOffice = response.json()["BoxOffice"]
    
    pairs.append(temp)
    
    print(temp.awards, temp.tomatoes, temp.metascore, temp.production, temp.boxOffice)
    
    print(pairs)
    object_list = list(pairs)
    nonetype_querySet = MovieObj.objects.none()
    
    data = list(chain(nonetype_querySet, object_list))
    
    data = serializers.serialize('json', data)
    print(data)
    return render_to_response("details.html", {'data': mark_safe(data)}, RequestContext(request))    

def general(request):
    data = MovieObj.objects.all()

    print(data)

    for obj in data:
        obj.title = titlecase(obj.title)
        obj.title.replace(" ,", "")

    data = serializers.serialize('json', data)

    genreset = set()
    
    with open('explore/genre.txt') as f:
        lines = f.readlines()
        
        for line in lines:
            line = line.replace("\n","")
            arr = line.split('|')
            for word in arr:
                genreset.add(word)
               
    return render_to_response("general.html", {'data': mark_safe(data), 'genre' : list(genreset)}, RequestContext(request))

def response(request, results):
    pairs = []
    for i in results:
        movie = MovieObj()
        temp = get_object_or_404(MovieObj, movieID=str(i[0]))
        temp.relevance = i[1]
        print(str(i[0] + str("NO F***** API CALLS")))
        temp.criteria = i[2]
        pairs.append(temp)

    print(pairs)
    object_list = list(pairs)
    nonetype_querySet = MovieObj.objects.none()

    data = list(chain(nonetype_querySet, object_list))

    for obj in data:
        obj.title = titlecase(obj.title)
        obj.title.replace(" ,", "")

    data = serializers.serialize('json', data)

    return render_to_response("cloudResults.html", {'data': mark_safe(data)}, RequestContext(request))