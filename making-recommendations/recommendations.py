# A dictionary of movie critics and their ratings of a small
# set of movies
critics={'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
 'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5,
 'The Night Listener': 3.0},
'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5,
 'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0,
 'You, Me and Dupree': 3.5},
'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
 'Superman Returns': 3.5, 'The Night Listener': 4.0},
'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
 'The Night Listener': 4.5, 'Superman Returns': 4.0,
 'You, Me and Dupree': 2.5},
'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
 'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
 'You, Me and Dupree': 2.0},
'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
 'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
'Toby': {'Snakes on a Plane':4.5,'You, Me and Dupree':1.0,'Superman Returns':4.0}}

from math import sqrt 
# Gets distance between person1 and person2
def sim_distance(prefs,person1,person2):
        # Get the list of shared_tems
        si={}
        for item in prefs[person1]:
            if item in prefs[person2]:
                si[item]=1
        # return 0 if both the person has no preferance        
        if len(si)==0: return 0

        sum_of_squares=sum([pow(prefs[person1][item]-prefs[person2][item],2) for item in prefs[person1] if item in prefs[person2]])

        return 1/(1+sum_of_squares)

# Returns pearsons correlation
def pearson_correlation(prefs,person1,person2):
    si={}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item]=1
    if len(si)==0: return 0

    # Added up all the preferences
    sum1=sum([prefs[person1][it] for it in si])
    sum2=sum([prefs[person2][it] for it in si])

    # Sum of the squares
    sumSq1=sum(pow(prefs[person1][it],2) for it in si)
    sumSq2=sum(pow(prefs[person2][it],2) for it in si)

    # Sum of the products
    pSum=sum(prefs[person1][it]*prefs[person2][it] for it in si)

    # Calculating Pearson Score
    num=pSum-(sum1*sum2/len(si))
    den=sqrt((sumSq1-pow(sum1,2)/len(si))*(sumSq2-pow(sum2,2)/len(si)))
    if den==0: return 0
    r=num/den
    return r

# Returns the best matches for person from the data set
def top_matches(prefs,person,n=5,similarity=pearson_correlation):
    scores=[(similarity(prefs,person,other),other) for other in prefs if other!=person]

    # Sorting the list to get the highest scores first
    scores.sort()
    scores.reverse()
    return scores[0:n]

# Get recommendations for a person by using a weight average of every other user's rankings

def getRecommendations(prefs, person, similarity=pearson_correlation):
    totals={}
    simSums={}
    for other in prefs:

        if other == person: continue
        sim=similarity(prefs,person,other)

        if sim<=0: continue

        # check only the movies that I have not watched
        for item in prefs[other]:
            if item not in prefs[person] or prefs[person][item]==0:
                # Similarity * score
                totals.setdefault(item,0)
                totals[item] += prefs[other][item]*sim

                # SUm of similarities
                simSums.setdefault(item,0)
                simSums[item]+=sim
    rankings = [(total/simSums[item],item) for item,total in totals.items()]

    # returning the sorted list
    rankings.sort()
    rankings.reverse()
    return rankings

# Function to transform the critics data set to movie person
def transformPrefs(prefs):
    result={}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item,{})

            # Flip item and person
            result[item][person] = prefs[person][item]
    return result    


def loadMovieLens(path='../datasets/movielens'):

    # Get movie titles
    movies={}
    for line in open(path+"/u.item", encoding = "ISO-8859-1"):
        (id,title)=line.split('|')[0:2]
        movies[id]=title

    # Load data
    prefs={}
    for line in open(path+"/u.data", encoding = "ISO-8859-1"):
        (user,movieid,rating,ts)=line.split('\t')
        prefs.setdefault(user,{})
        prefs[user][movies[movieid]]=float(rating)
    return prefs        