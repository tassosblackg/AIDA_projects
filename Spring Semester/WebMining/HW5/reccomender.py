import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

## Read data with ratings
movies_ratings = pd.read_csv("ml-latest-small/ratings.csv")

print(movies_ratings)

# Group by userID, mean ratings of all movies for one user
mean_ratings_per_user = movies_ratings.groupby(by="userId", as_index=False)[
    "rating"
].mean()


# Merge two dataframes based on userId
Rating_avg = pd.merge(movies_ratings, mean_ratings_per_user, on="userId")
# print(Rating_avg[Rating_avg["userId"] == 1])
Rating_avg["adg_rating"] = (
    Rating_avg["rating_x"] - Rating_avg["rating_y"]
)  # normalize ratings using user avg rating for all movies
print(Rating_avg)

user_movie_rating_table = pd.pivot_table(
    Rating_avg, values="adg_rating", index="userId", columns="movieId"
)
print(user_movie_rating_table)


# Because not all the users have seen all the movies there are nul values
final_user_movie_rating_table = user_movie_rating_table.fillna(
    user_movie_rating_table.mean(axis=0)
)
print("Fill the NAN cells with avg of movies' rating \n", final_user_movie_rating_table)

# print(final_user_movie_rating_table.corr("pearson"))
full_table_pearson_corr = final_user_movie_rating_table.corr("pearson")
