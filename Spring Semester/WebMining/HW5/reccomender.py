import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import train_test_split
import time

# start_time = time.time()

## Read data with ratings
movies_ratings = pd.read_csv("ml-latest-small/ratings.csv")
print(movies_ratings)
movies_ratings_train, movies_ratings_test = train_test_split(
    movies_ratings, test_size=0.1, shuffle=True, random_state=5
)
print(movies_ratings_test)

# Group by userID, mean ratings of all movies for one user
mean_ratings_per_user = movies_ratings_test.groupby(by="userId", as_index=False)[
    "rating"
].mean()


# Merge two dataframes based on userId
Rating_avg = pd.merge(movies_ratings, mean_ratings_per_user, on="userId")
print("Merged dataframes \n", Rating_avg.head())
# # print(Rating_avg[Rating_avg["userId"] == 1])
Rating_avg["adg_rating"] = (
    Rating_avg["rating_x"] - Rating_avg["rating_y"]
)  # normalize ratings using user avg rating for all movies
# print(Rating_avg)

user_movie_rating_table = pd.pivot_table(
    Rating_avg, values="adg_rating", index="userId", columns="movieId"
)
print(user_movie_rating_table.head())
#
#
# Because not all the users have seen all the movies there are nul values
final_user_movie_table = user_movie_rating_table.fillna(
    user_movie_rating_table.mean(axis=0)
)
print("Fill the NAN cells with avg of movies' rating \n", final_user_movie_table.head())

# Pearson Correlation between Users
pearson_corr_user = final_user_movie_table.T.corr(
    "pearson"
)  # get the rows' correlations
print("Pearson correlation \n", pearson_corr_user.head())

print("Size ", pearson_corr_user.shape)

# print(final_user_movie_rating_table.corr("pearson"))
# full_table_pearson_corr = final_user_movie_rating_table.corr("pearson")
# print(full_table_pearson_corr.head())
#
# # Find N similar users
# def find_n_neighbours(df, n):
#     order = np.argsort(df.values, axis=1)[:, :n]
#     print(order)
#     # df = df.apply(
#     #     lambda x: pd.Series(
#     #         x.sort_values(ascending=False).iloc[:n].index,
#     #         index=["top{}".format(i) for i in range(1, n + 1)],
#     #     ),
#     #     axis=1,
#     # )
#     return df
#
#
# dd = find_n_neighbours(full_table_pearson_corr, 10)
# print(dd)
# end_time = time.time()
# print("Duration: {}".format(end_time - start_time))
