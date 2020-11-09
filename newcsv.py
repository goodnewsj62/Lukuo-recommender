import pandas as pd
f=pd.read_csv("./tmdb.csv")
keep_col = ["title",
    "homepage",
    "cast",
    "crew",
    "release_date",
    "original_language",
    "production_countries",
    "tagline",
    "genres" ,
    "overview",
    "director",
    "vote_count",
    "vote_average",
    "keywords",
    "soup" ]
new_f = f[keep_col]
new_f.to_csv("newtmdb.csv", index=False)

