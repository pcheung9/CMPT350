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


def search(request):
    return TemplateResponse(request, 'search.html')

def results(request):
    name = request.GET['search']
    IDs = stringBuilder(name)
    results = related(15, IDs, 1, 1, 1, 1, 1)
    pairs = []
    
    resultsList = results.split()

    for pair in resultsList:
        movie = MovieObj()
        split = pair.split('|')
        temp = get_object_or_404(MovieObj, movieID=str(split[0]))
        temp.relevance = split[1]
        pairs.append(temp)

    print(pairs)
    object_list = list(pairs)
    nonetype_querySet = MovieObj.objects.none()

    data = list(chain(nonetype_querySet, object_list))

    json_data = serializers.serialize('json', data)
    print(json_data)
    return TemplateResponse(request, 'results.html', {"data": json_data})

def test(request, json_data):
    return TemplateResponse(request, 'results.html')