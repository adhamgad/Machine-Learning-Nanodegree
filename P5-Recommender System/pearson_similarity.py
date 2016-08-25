from math import sqrt
import numpy as np 

def pearson_sim(train,user_a,user_b):

    """Computes pearson similarity between user a and user b and returns a float value between 1 and -1"""
    avg_ratings = train.groupby("user_id").agg({"rating":np.mean}).reset_index()
    userA_avg = avg_ratings.loc[avg_ratings["user_id"] == user_a].rating.values[0] #mean of user A ratings
    userB_avg = avg_ratings.loc[avg_ratings["user_id"] == user_b].rating.values[0] #mean of user B ratings
    
    userA_movies_ratings = train.loc[train["user_id"] == user_a] 
    userB_movies_ratings = train.loc[train["user_id"] == user_b]
    

    diff_squaredA = []
    diff_squaredB = []
    flag = 0

    
    #for each movie watched by two users we calculate each user's rating minus the mean
    
    """
    for indexA,valA in userA_movies_ratings.iterrows():
        for indexB,valB in userB_movies_ratings.iterrows():
            if valA["movie_id"] == valB["movie_id"]:
                tempA = valA["rating"]-userA_avg
                diffA.append(tempA)
                tempB =valB["rating"]-userB_avg 
                diffB.append(tempB)
                diff_squaredA.append(pow(tempA,2)) 
                diff_squaredB.append(pow(tempB,2))
                

                
    """
    userA_common = userA_movies_ratings.loc[userA_movies_ratings['movie_id'].isin(userB_movies_ratings["movie_id"].values)] #user A ratings for common movies
    userB_common = userB_movies_ratings.loc[userB_movies_ratings['movie_id'].isin(userA_movies_ratings["movie_id"].values)] #user B ratings for common movies
    
    diffA = userA_common.rating - userA_avg #difference between user A ratings and user A average rating
    diffB = userB_common.rating - userB_avg #difference between user B ratings and user B average rating
    diffA = diffA.values
    diffB = diffB.values
    #calculate the square of differences
    diff_squaredA = (pow(diffA,2)) 
    diff_squaredB = (pow(diffB,2))
     
    num = []
    den = []
    for i in range(len(diffA)):
        #calculate the numerator of the predict equation
        num.append(diffA[i]*diffB[i])

    num = sum(num)
    #calculate the denominator of the predict equation
    den = sqrt(sum(diff_squaredA))*sqrt(sum(diff_squaredB))
    
    if den == 0:
        return 0
    else:
        return num/den 
    


