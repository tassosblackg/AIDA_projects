import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from scipy.spatial.distance import cosine
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import time

TRAIN_SIZE = 0.9
TEST_SIZE = 0.1
K = 30


## Read data with ratings
movies_ratings = pd.read_csv("ml-latest-small/ratings.csv")
print(movies_ratings.head())

movies_ratings_train, movies_ratings_test = train_test_split(
    movies_ratings,
    train_size=TRAIN_SIZE,
    test_size=TEST_SIZE,
    shuffle=True,
    random_state=5,
)
print(
    "\nTrain set : \n",
    movies_ratings_train.head(),
    "\nTest set : \n",
    movies_ratings_test.head(),
)

# Group by userID, mean ratings of all movies for one user
mean_ratings_per_user = movies_ratings_train.groupby(by="userId", as_index=False)[
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


# # Find N similar users
def find_n_neighbours(df, n):
    order = np.argsort(df.values, axis=1)[:, :n]
    # print(order)
    df = df.apply(
        lambda x: pd.Series(
            x.sort_values(ascending=False).iloc[:n].index,
            index=["top{}".format(i) for i in range(1, n + 1)],
        ),
        axis=1,
    )
    return df


dd = find_n_neighbours(pearson_corr_user, K)
print("\nK-NN user based  \n", dd)


## Item based
# Group by movieID, mean ratings of all movies for one user
mean_ratings_per_item = movies_ratings_train.groupby(by="movieId", as_index=False)[
    "rating"
].mean()
# Merge two dataframes based on userId
rating_avg_items = pd.merge(movies_ratings, mean_ratings_per_item, on="movieId")
print("Merged item-based dataframes \n", rating_avg_items.head())

rating_avg_items["adg_rating"] = (
    rating_avg_items["rating_x"] - rating_avg_items["rating_y"]
)  # normalize ratings using user avg rating for all movies
# print(rating_avg_items.head())

user_movie_rating_table2 = pd.pivot_table(
    Rating_avg, values="adg_rating", index="userId", columns="movieId"
)
print(user_movie_rating_table2.head())
final_items_table = user_movie_rating_table2.fillna(
    user_movie_rating_table2.mean(axis=0)
)
print(final_items_table.head())
print(final_items_table.shape[1])
# print(final_items_table[0, :])
pivot2df = final_items_table.reset_index()
m, n = pivot2df.shape[0], pivot2df.shape[1]  # users, movies
items_sim = np.zeros((n, n))
# print("@", pivot2df.head(), pivot2df.shape)

# for i in range(n):
#     for j in range(n):
#         if i != j:
#             items_sim[i][j] = cosine_similarity(pivot2df[:, i], pivot2df[:, j])
#         else:
#             items_sim[i][j] = 0.0
#
# print("\nItems sim = \n", items_sim)
