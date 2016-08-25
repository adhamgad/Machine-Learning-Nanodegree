import operator 
from pearson_similarity import pearson_sim 
import numpy as np 
def predict(train,user_a,movie_id,sim_threshold):
    """takes user id and movie id and computes user's prediction on that movie"""
    reduced = train[:] #this is used while developing to reduce the size of the dataset if needed
    #print reduced
    avg_ratings = reduced.groupby("user_id").agg({"rating":np.mean}).reset_index()
    userA_avg = avg_ratings.loc[avg_ratings["user_id"] == user_a].rating.values[0]
    
    numerator = []
    denominator = []
    
    removed_duplicates = reduced.drop_duplicates("user_id") 
    #print removed_duplicates
    userA_data = reduced.loc[reduced["user_id"] == user_a]
    #print userA_data
    for indexB,valB in removed_duplicates.iterrows():
        if valB["user_id"] != user_a: #if not the active user enter 
            #get ri,j which is the rating of user i on movie j
            temp = reduced.loc[reduced["user_id"] == valB["user_id"]]
            rating = temp.loc[temp["movie_id"] == movie_id]
            
            if len(rating)==0:
                #print "movie not rated by the other user"
                continue
            
            sim = pearson_sim(train,user_a,valB["user_id"])
            if sim <= sim_threshold:
                #break if similarity is less than or equals zero
                #print "sim"
                continue 
            
            #if movie_id in userA_data.movie_id.values:
                #movie is already rated by the user
                #this is only commented here for testing purposes as we test on movie that's already rated by the user to be able to calculate errors
                #if this code went to production we should skip this loop as we shouldnt predict movies already rated
                #print "duplicate"
                #continue 
                
            
            #sim[valB["user_id"]] = pearson_sim(1,valB["user_id"])
            userB_avg = avg_ratings.loc[avg_ratings["user_id"] == valB["user_id"]].rating.values[0] #user average ratings
            #print userB_avg

            
            rating = temp.loc[temp["movie_id"] == movie_id].rating.values[0]
            rating = rating - userB_avg
            numerator.append(sim * rating)
            denominator.append(sim)

    numerator = sum(numerator)
    denominator = sum(denominator)
    #print denominator
    if denominator == 0:
        return 0
    else:
        return userA_avg + (numerator/denominator)
