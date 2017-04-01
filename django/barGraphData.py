from explore.models import MovieObj
import os
import sys
import csv

movies = MovieObj.objects.all()

with open('movie.csv', 'r', encoding="utf8") as csvfile:
    CSVreader = csv.reader(csvfile)
    for row in CSVreader:
            for movie in movies:
                if movie.movieID == row[28]:
                    if row[2] != '':
                        movie.numCritic = row[2]
                        #print(movie.IMDBScore)
                    if row[8] != '':
                        movie.gross = row[8]
                       # print(movie.gross)
                    if row[13] != '':
                        movie.fblikes = row[13]
                        #print(movie.fblikes)
                    if row[22] != '':
                        movie.budget = row[22]
                       # print(movie.budget)
                    if row[18] != '':
                        movie.numReviews = row[18]
                        #print(movie.numReviews)
                    if row[25] != '':
                        movie.IMDBScore = float(row[25])
                        #print(movie.IMDBScore)
                    movie.save()

for movie in movies:
    print("Number of Critics:" , movie.numCritic)
    print("Gross:", movie.gross)
    print("FB Likes:" , movie.fblikes)
    print("Budget:" , movie.numReviews)
    print("Number of Review:" , movie.numReviews)
    print("IMDB SCore:" , movie.IMDBScore)