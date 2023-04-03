import numpy as np
import pandas as pd
import datetime

data = pd.read_csv("netflix_titles.csv")
print(data.head())

print(data.shape)
# (8807, 12)

print(list(data.columns))
# ['show_id', 'type', 'title', m'director', m'cast', m'country', m'date_added',
#  'release_year', m'rating', m'duration', 'listed_in', 'description']  12

print(data.isnull().mean())
print(data.isnull().count())
print(list(data.notnull().columns))
print(data.describe())
print(data.info())

print(data.dtypes)

str_cols = list(data.columns)
str_cols.remove("release_year")
print(str_cols)

for i in str_cols:
    data[i] = data[i].str.strip()
    
print(str_cols)

columns = ['director', 'cast', 'country', 'raring', 'date_added']

for column in columns:
    data[column] = data[column].fillna("")

# examining rows with null values for date_added column 
rows = []
for i in range(len(data)):
    if data['date_added'].iloc[i] == "":
        rows.append(i)
        
# examine those rows to confirm null state
data.loc[rows, :]

# extracting months added and years added
month_added = []
year_added = []

for i in range(len(data)):
    # replacing NaN values with 0
    if i in rows:
        month_added.append(0)
        year_added.append(0)
    else:
        date = data["date_added"].iloc[i].split(" ")
        month_added.append(date[0])
        year_added.append(date[2])
        
# turning month names into month numbers
for i,month in enumerate(month_added):
    if month != 0:
        datetime_obj = datetime.strptime(month, "%B")
        month_number = datetime_obj.month
        month_added[i] = month_number
        
# checking all months
print(set(month_added))
print(set(year_added))

# inserting the month and year columns into the dataset
data.insert(7, "month_added", month_added, allow_duplicates=True)
data.insert(8, "year_added", year_added, allow_duplicates=True)
print(data.head())

# seprating original dataset to tv show and movie dataset respectively
shows = []
films = []

# looping through the dataset to identify rows that are TV shows and films
for i in range(len(data)):
    if data['type'].iloc[i] == "TV Show":
        shows.append(i)
    else:
        films.append(i)
        
# grouping rows that are TV shows
netflix_shows = data.loc[shows, : ]
netflix_films = data.loc[films, : ]

# reseting the index of the datasets
netflix_shows = netflix_shows.set_index([pd.Index(range(0, len(netflix_shows)))])
netflix_films = netflix_films.set_index([pd.Index(range(0, len(netflix_films)))])

# get length of movie or number of seasons of show
def getDuration(data1):
    count = 0
    durations = []
    for value in data1:
        # filling in missing values
        if type(value) is float:
            durations.append(0)
        else:
            values = value.split(" ")
            durations.append(int(values[0]))
    return durations

# inserting new duration type column for shows (renamed column)
netflix_shows.insert(11, 'season', getDuration(netflix_shows['duration']))
netflix_shows = netflix_shows.drop(['duration'], axis=1)
netflix_shows.head()

# inserting new duration type column for films (renamed column)
netflix_films.insert(11, 'length', getDuration(netflix_films['duration']))
netflix_films = netflix_films.drop(['duration'], axis=1)
netflix_films.head()

# getting the unique ratings for films
netflix_films['rating'].unique()

# getting the unique ratings for shows
netflix_shows['rating'].unique()

# printing more details of the rows that have incorrect ratings
incorrect_ratings = ['74 min','84 min', '66 min']
for i in range(len(netflix_films)):
    if netflix_films['rating'].iloc[i] in incorrect_ratings:
        print(netflix_films.iloc[i])
        print("")
        
# getting the row indices
index = [3562, 3738, 3747]

# fixing the entries
for i in index:
    split_value = netflix_films['rating'].iloc[i].split(" ")
    length = split_value[0]
    netflix_films['duration'].iloc[i] = length
    netflix_films['rating'].iloc[i] = "NR"
    
# double checking the entries again
for i in index:
    print(netflix_films.iloc[i])
    
# fixing the entries
for i in range(len(netflix_films)):
    if netflix_films['rating'].iloc[i] == "UR":
        netflix_films['rating'].iloc[i] == "NR"
        
# double checking
netflix_films['rating'].unique()

# function to get unique values of a column
def getUnique(data1):
    unique_values = set()
    for value in data1:
        if type(value) is float:
            unique_values.add(None)
        else:
            values = value.split(" ,")
            for i in values:
                unique_values.add(i)
    return list(unique_values)

# getting unique country names
unique_countries = getUnique(data['country'])
print(unique_countries)

# converting soviet union to russia and east/west germany to germany
for i in range(len(data)):
    if type(data['country'].iloc[i]) is not float:
        countries = data['country'].iloc[i].split(", ")
        for j in range(len(countries)):
            if "Germany" in countries[j]:
                countries[j] = "Germany"
            elif "Soviet Union" in countries[j]:
                countries[j] = "Russia"
        data['country'].iloc[i] = ", ".join(countries)
        
# getting unique film genres
unique_genres_films = getUnique(netflix_films['listed_in'])
print(unique_genres_films)

# getting unique show genres
unique_genres_shows = getUnique(netflix_shows['listed_in'])
print(unique_genres_shows)

# checking for TV shows

# replace netflix_shows with netflix_films to check for movies
count = 0
index = []
for i, value in enumerate(netflix_shows['listed_in']):
    genres = value.split(", ")
    if "TV Shows" in genres:
        count += 1
        index.append(i)

print("count %s" %count)
print("index %s" %index)

# printing the first 5 rows of all that have TV shows as its genre
print(netflix_shows.iloc[index[0:5]])

# printing the first 5 rows of all rows that have Movies as its genre
print(netflix_films.iloc[index[0:5]])