from django.shortcuts import render, render_to_response, get_object_or_404
from django.template.loader import render_to_string
import random


# Create your views here.
from django.http import HttpResponse
from django.http import JsonResponse
from explore.models import MovieObj
from django.template.response import TemplateResponse
import json
from django.core import serializers
from itertools import chain
from explore.algorithm import *

def load(request):
    data = {}
    data = MovieObj.objects.all()
    json_data = serializers.serialize('json', data)
    print("Test console output")
    return HttpResponse(json_data, content_type="application/json")

def indexView(request):
    return TemplateResponse(request, 'search.html')



def explore(request):
    IDs = stringBuilder()
    results = related(15, IDs)
    pairs = []
    idList = []
    
    resultsList = results.split()

    for pair in resultsList:
        movie = MovieObj()
        split = pair.split('|')
        temp = get_object_or_404(MovieObj, movieID=str(split[0]))
        temp.relevance = split[1]

        #print(temp.movieID + ' ' + temp.title + ' ' + temp.relevance)
        #print(pairs)
        pairs.append(temp)


    print(pairs)

    object_list = list(pairs)
    nonetype_querySet = MovieObj.objects.none()
    
    #generate queryset somehow?
    data = {}
    data = list(chain(nonetype_querySet, object_list))

    json_data = serializers.serialize('json', data)
    return TemplateResponse(request, 'explore.html', {"data": json_data})


# makes movie object from models.py for saving into sqlite database out of Movie() class.
def makeMovieObj(temp):
    movie = MovieObj()

    movie.title = temp.title
    # movie.titleWords = temp.titleWords
    movie.year = temp.year
    movie.actor1 = temp.actor1
    movie.actor2 = temp.actor2
    movie.actor3 = temp.actor3
    movie.director = temp.director
    # movie.keywords = row[16].split('|')
    # movie.genres = row[9].split('|')
    movie.country = temp.country
    movie.language = temp.language
    movie.rating = temp.rating
    movie.score = temp.score
    movie.movieID = temp.ID
    # if count <= 4920:
    # global flag
    # flag = False
    movie.save()

