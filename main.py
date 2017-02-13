import csv
import bisect

ratings = {"Passed": 0, "Approved": 0, "Unrated": 0, "Not Rated": 0, "": 0,"TV-Y": 0, "TV-G": 1, "G": 1, "TV-Y7": 2, "GP": 2, "TV-PG": 2, "PG": 2, "TV-14": 3, "PG-13": 3, "TV-MA": 4, "M": 4, "R": 4, "NC-17": 4, "X": 5}
common = ["the", "and", "of"]
class movie:
    def __init__(self):
        self.rating = 0
        self.title = ""
        self.titleWords = []
        self.year = 0
        self.actor1 = ""
        self.actor2 = ""
        self.actor3 = ""
        self.director = ""
        self.keywords = []
        self.genres = []
        self.relevance = 0
        self.country = ""
        self.language = ""
        self.criteria = []
        self.rating = 0
        self.score = 0

    def __lt__(self, other):
        return self.relevance > other.relevance

inputs = []
movies = []
with open('movieDB.txt', 'r', encoding="utf8") as csvfile:
    CSVreader = csv.reader(csvfile, delimiter='\t', quotechar='"', skipinitialspace=True)
    count = 0
    for row in CSVreader:
        if count != 0:
            temp = movie()
            temp.rating = float(row[25])
            temp.title = row[11][:-1].lower()
            temp.titleWords = []
            for i in row[11][:-1].lower().split():
                if i not in common:
                    temp.titleWords.append(i)
            if row[23] != '':
                temp.year = int(row[23])
            temp.actor1 = row[10]
            temp.actor2 = row[6]
            temp.actor3 = row[14]
            temp.director = row[1]
            temp.keywords = row[16].split('|')
            temp.genres = row[9].split('|')
            temp.country = row[20]
            temp.language = row[19]
            temp.rating = ratings[row[21]]
            temp.score = float(row[25])

            movies.append(temp)
        count += 1

for i in movies:
    if i.title == "Robocop".lower():
        inputs.append(i)
        print(i.titleWords)
        print(i.genres)
        print(i.keywords)

for i in movies:
    if i.title == "Dredd".lower():
        inputs.append(i)
        print(i.titleWords)
        print(i.genres)
        print(i.keywords)


if len(inputs) < 2:
    exit(1)


relevance = []
top = []
for i in movies:
    for input in inputs:
        #Actor Check
        if i.actor1 == input.actor1 or i.actor1 == input.actor2 or i.actor1 == input.actor3:
            i.relevance += 35
            i.criteria.append("Actor: "+i.actor1)
        if i.actor2 == input.actor1 or i.actor2 == input.actor2 or i.actor2 == input.actor3:
            i.relevance += 35
            i.criteria.append("Actor: "+i.actor2)
        if i.actor3 == input.actor1 or i.actor3 == input.actor2 or i.actor3 == input.actor3:
            i.relevance += 35
            i.criteria.append("Actor: "+i.actor3)

        #Director Check
        if i.director == input.director:
            i.relevance = 35
            i.criteria.append("Director: "+i.director)

        #Country Check
        if i.country == input.country:
            i.relevance += 10
            i.criteria.append("country")

        #Language Check
        if i.language != input.language:
            i.relevance -= 50

        #Rating Check
        if i.rating != 0:
            if i.rating == input.rating:
                i.relevance += 20
            if i.rating == (input.rating + 1) or i.rating == (input.rating - 1):
                i.relevance += 10
            if i.rating == (input.rating + 3) or i.rating == (input.rating - 3):
                i.relevance -= 100
            if i.rating == (input.rating + 4) or i.rating == (input.rating - 4):
                i.relevance -= 200

        #Keyword Check
        for j in i.keywords:
            for k in input.keywords:
                if j == k:
                    i.relevance += 40
                    i.criteria.append("Keyword: "+j)

        #Genre Check
        for j in i.genres:
            for k in input.genres:
                if j == k:
                    i.relevance += 30
                    i.criteria.append("genre: "+j)

        #Title Check
        count = 0;
        for j in i.titleWords:
            if not j.isdigit():
                for k in input.titleWords:
                    if j == k:
                        count += 1
        if count > (len(input.titleWords)/3):
            i.criteria.append(str(count)+" Title words")
            i.relevance += 20

        #Year Check
        if (input.year - 5) <= i.year <= (input.year + 5):
            i.relevance += 10
            i.criteria.append("Year: 10")
        elif (input.year - 5) <= i.year <= (input.year + 5):
            i.relevance += 5
            i.criteria.append("Year: 5")

        #IMDB Score
        i.relevance += 3*i.score

        bisect.insort_right(top, i);


for i in range(0, 15):
    print(top[i].title, "%.2f" %top[i].relevance, top[i].criteria)

