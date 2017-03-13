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
    

def search(request):

    #search = request['search']
    data = {}
    if request.method == 'POST':
        if(request.POST['search_text'] != ''):
            print(request.POST['search_text'])
            object_list = list(request.POST)
            return explore(request, request.POST['search_text'])
        else:       
            print("Empty Search")
            print(request.POST['csrfmiddlewaretoken'])
            return explore(request, request.POST['search_text'])            

    #return TemplateResponse(request, 'search.html')

def explore(request, name):
    IDs = stringBuilder(name)
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