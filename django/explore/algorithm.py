import csv
import bisect
from explore.models import MovieObj

ratings = {"Passed": 0, "Approved": 0, "Unrated": 0, "Not Rated": 0, "": 0, "TV-Y": 0, "TV-G": 1,
           "G": 1, "TV-Y7": 2, "GP": 2, "TV-PG": 2, "PG": 2, "TV-14": 3, "PG-13": 3, "TV-MA": 4,
           "M": 4, "R": 4, "NC-17": 4, "X": 5}

common = ["the", "and", "of"]  # List of common words to be filtered from titles
flag = True


class Movie:
    def __init__(self):
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
        self.ID = ""

    def __lt__(self, other):
        return self.relevance > other.relevance


# Function Name: reader()
# Function Purpose: This block of code reads the entire TSV file and stores each movie in an object
# Parameters:
#   fileName: The name of the TSV file
def reader(fileName):
    global flag
    movies = []

    count = 0
    with open(fileName, 'r', encoding="utf8") as csvfile:
        TSVreader = csv.reader(csvfile, delimiter='\t', quotechar='"', skipinitialspace=True)
        for row in TSVreader:
            temp = Movie()
            if not count <= 1:  # Makes sure the headers aren't stored in an object

                # temp = Movie()  # Creates a temp object
                temp.title = row[11][:-1].lower()  # Converts all titles to lower and strips off end char

                # Puts any non-common title words into a list
                temp.titleWords = []
                for i in row[11][:-1].lower().split():
                    if i not in common:
                        temp.titleWords.append(i)

                # Error checks for rows without years
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
                temp.ID = row[28].lower()

                movies.append(temp)
                if(flag):
                    makeMovieObj(temp)
                    print(temp)
                # uncomment if you want to repopulate the database from scratch for some reason. Or, load the fixture like a reasonable human.
            count += 1
            print(count)
    # flag = False
    return (movies)



# Function Name: Related
# Function Purpose: Takes an input string of IMDB ID's and returns the top 15 most related films
# Parameters:
#   num_results: The number of results to be returned
#   ID_string: The string containing IMDB IDs
def related(num_results, ID_string):
    listIDs = ID_string.split(" ")  # Splits inFilm string into list of IDs
    movies = reader("movieDB.txt")

    # Populates
    inputs = []
    for i in movies:
        for j in listIDs:
            if i.ID == j:
                inputs.append(i)
                print(i.titleWords)
                print(i.genres)
                print(i.keywords)

    top = []
    for i in movies:
        for inFilm in inputs:
            # Actor Check
            if i.actor1 == inFilm.actor1 or i.actor1 == inFilm.actor2 or i.actor1 == inFilm.actor3:
                i.relevance += 35
                i.criteria.append("Actor: " + i.actor1)
            if i.actor2 == inFilm.actor1 or i.actor2 == inFilm.actor2 or i.actor2 == inFilm.actor3:
                i.relevance += 35
                i.criteria.append("Actor: " + i.actor2)
            if i.actor3 == inFilm.actor1 or i.actor3 == inFilm.actor2 or i.actor3 == inFilm.actor3:
                i.relevance += 35
                i.criteria.append("Actor: " + i.actor3)

            # Director Check
            if i.director == inFilm.director:
                i.relevance = 35
                i.criteria.append("Director: " + i.director)

            # Country Check
            if i.country == inFilm.country:
                i.relevance += 10
                i.criteria.append("country")

            # Language Check
            if i.language != inFilm.language:
                i.relevance -= 50

            # Rating Check
            if i.rating != 0:
                if i.rating == inFilm.rating:
                    i.relevance += 20
                if i.rating == (inFilm.rating + 1) or i.rating == (inFilm.rating - 1):
                    i.relevance += 10
                if i.rating == (inFilm.rating + 3) or i.rating == (inFilm.rating - 3):
                    i.relevance -= 100
                if i.rating == (inFilm.rating + 4) or i.rating == (inFilm.rating - 4):
                    i.relevance -= 200

            # Keyword Check
            for j in i.keywords:
                for k in inFilm.keywords:
                    if j == k:
                        i.relevance += 40
                        i.criteria.append("Keyword: " + j)

            # Genre Check
            for j in i.genres:
                for k in inFilm.genres:
                    if j == k:
                        i.relevance += 30
                        i.criteria.append("genre: " + j)

            # Title Check
            count = 0
            for j in i.titleWords:
                if not j.isdigit():
                    for k in inFilm.titleWords:
                        if j == k:
                            count += 1
            if count > (len(inFilm.titleWords) / 3):
                i.criteria.append(str(count) + " Title words")
                i.relevance += 20

            # Year Check
            if (inFilm.year - 5) <= i.year <= (inFilm.year + 5):
                i.relevance += 10
                i.criteria.append("Year: 10")
            elif (inFilm.year - 5) <= i.year <= (inFilm.year + 5):
                i.relevance += 5
                i.criteria.append("Year: 5")

            # IMDB Score
            i.relevance += 3 * i.score

        bisect.insort_right(top, i)

    # for i in range(0, num_results):
    #   print(top[i].title, "%.2f" % top[i].relevance, top[i].criteria)
    topN = []
    for i in range(0, num_results):
        topN.append("" + top[i].ID + "|" + str(top[i].relevance) + "")
    topString = " ".join(topN[:15])
    return topString


# Temp function. Use to make generate input strings for now. Enter names into array.
def stringBuilder(name):
    movies = reader("movieDB.txt")
    inputs = [name]
    IDs = []
    for j in inputs:
        for i in movies:
            if i.title.lower() == j.lower():
                IDs.append(i.ID)
    print(IDs)
    return " ".join(IDs)


class Movie:
    def __init__(self):
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
        self.ID = ""

    def __lt__(self, other):
        return self.relevance > other.relevance

# Function Name: reader()
# Function Purpose: This block of code reads the entire TSV file and stores each movie in an object
# Parameters:
#   fileName: The name of the TSV file
def reader(fileName):
    global flag
    movies = []

    count = 0
    with open(fileName, 'r', encoding="utf8") as csvfile:
        TSVreader = csv.reader(csvfile, delimiter='\t', quotechar='"', skipinitialspace=True)
        for row in TSVreader:
            temp = Movie()
            if not count <= 1:  # Makes sure the headers aren't stored in an object

                #temp = Movie()  # Creates a temp object
                temp.title = row[11][:-1].lower()  # Converts all titles to lower and strips off end char

                # Puts any non-common title words into a list
                temp.titleWords = []
                for i in row[11][:-1].lower().split():
                    if i not in common:
                        temp.titleWords.append(i)

                # Error checks for rows without years
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
                temp.ID = row[28].lower()



                movies.append(temp)
            #if(flag):
                #makeMovieObj(temp)
                #print(temp)
                # uncomment if you want to repopulate the database from scratch for some reason. Or, load the fixture like a reasonable human.
            count += 1
    flag = False
    return(movies)


# Function Name: Related
# Function Purpose: Takes an input string of IMDB ID's and returns the top 15 most related films
# Parameters:
#   num_results: The number of results to be returned
#   ID_string: The string containing IMDB IDs
def related(num_results, ID_string, genreWeight, actorWeight, directorWeight, yearWeight, scoreWeight):

    listIDs = ID_string.split(" ")  # Splits inFilm string into list of IDs
    movies = reader("movieDB.txt")

    # Populates
    inputs = []
    for i in movies:
        for j in listIDs:
            if i.ID == j:
                inputs.append(i)
                print(i.titleWords)
                print(i.genres)
                print(i.keywords)
                print()

    top = []
    for i in movies:
        for inFilm in inputs:
            # Actor Check
            if i.actor1 == inFilm.actor1 or i.actor1 == inFilm.actor2 or i.actor1 == inFilm.actor3:
                i.relevance += (35 * actorWeight)
                i.criteria.append("Actor: "+i.actor1)
            if i.actor2 == inFilm.actor1 or i.actor2 == inFilm.actor2 or i.actor2 == inFilm.actor3:
                i.relevance += (35 * actorWeight)
                i.criteria.append("Actor: "+i.actor2)
            if i.actor3 == inFilm.actor1 or i.actor3 == inFilm.actor2 or i.actor3 == inFilm.actor3:
                i.relevance += (35 * actorWeight)
                i.criteria.append("Actor: "+i.actor3)

            # Director Check
            if i.director == inFilm.director:
                i.relevance += (35 * directorWeight)
                i.criteria.append("Director: "+i.director)

            # Country Check
            if i.country == inFilm.country:
                i.relevance += 10
                i.criteria.append("country")

            # Language Check
            if i.language != inFilm.language:
                i.relevance -= 50

            # Rating Check
            if i.rating != 0:
                if i.rating == inFilm.rating:
                    i.relevance += 20
                if i.rating == (inFilm.rating + 1) or i.rating == (inFilm.rating - 1):
                    i.relevance += 10
                if i.rating == (inFilm.rating + 3) or i.rating == (inFilm.rating - 3):
                    i.relevance -= 100
                if i.rating == (inFilm.rating + 4) or i.rating == (inFilm.rating - 4):
                    i.relevance -= 200

            # Keyword Check
            for j in i.keywords:
                for k in inFilm.keywords:
                    if j == k:
                        i.relevance += 40
                        i.criteria.append("Keyword: "+j)

            # Genre Check
            for j in i.genres:
                for k in inFilm.genres:
                    if j == k:
                        i.relevance += (30 * genreWeight)
                        i.criteria.append("genre: "+j)

            # Title Check
            count = 0
            for j in i.titleWords:
                if not j.isdigit():
                    for k in inFilm.titleWords:
                        if j == k:
                            count += 1
            if count > (len(inFilm.titleWords)/3):
                i.criteria.append(str(count)+" Title words")
                i.relevance += 20

            # Year Check
            if (inFilm.year - 5) <= i.year <= (inFilm.year + 5):
                i.relevance += (10 * yearWeight)
                i.criteria.append("Year: 10")
            elif (inFilm.year - 5) <= i.year <= (inFilm.year + 5):
                i.relevance += (5 * yearWeight)
                i.criteria.append("Year: 5")

            # IMDB Score
            i.relevance += ((3*i.score) * scoreWeight)

            bisect.insort_right(top, i)
    topN = []
    for i in range(0, num_results):
        topN.append("" + top[i].ID + "|" + str(top[i].relevance) + "")
    topString = " ".join(topN[:15])
    return topString

# Temp function. Use to make generate input strings for now. Enter names into array.
def stringBuilder(name):
    movies = reader("movieDB.txt")
    inputs = [name]
    IDs = []
    for j in inputs:
        for i in movies:
            if i.title.lower() == j.lower():
                IDs.append(i.ID)
    print(IDs)
    return " ".join(IDs)


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
    #if count <= 4920:
    #    global flag
    #    flag = False
    movie.save()
