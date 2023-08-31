# #!/usr/bin/env python3

# #################### ALWAYS RUN THIS FILE FIRST ####################
# import pandas as pd
# from sklearn.cluster import KMeans

# # # load cities coordinates (*BACKUP only if citiesCoordinate.csv is not available*)
# # data = {"location":[],"Latitude":[],"Longitude":[]}
# # with open("CORE/static/CORE/coordinates.csv", "r") as f:
# #   for line in f.readlines():
# #     line=line.strip("\n").split(",")
# #     data["location"].append(line[1].strip('"'))
# #     data["Latitude"].append(line[-2])
# #     data["Longitude"].append(line[-1])
# # dataset = pd.DataFrame(data)
# # dataset.to_csv("CORE/static/CORE/citiesCoordinate.csv", index=False)

# dataset = pd.read_csv("CORE/static/CORE/citiesCoordinate.csv")

# l2 = dataset.iloc[:,-1:-3:-1]
# # # print(l2)

# # # group around major 50 cities of india
# kmeans = KMeans(n_init=200, n_clusters=50, random_state=42)
# kmeans.fit(l2)

# identified_clusters = kmeans.fit_predict(l2)
# identified_clusters = list(identified_clusters)

# dataset['loc_clusters'] = identified_clusters
# ################################################################################


# def getCityList(city):
#   result = []
#   try:
#     input_city = city.lower().capitalize()
#     cluster = dataset.loc[dataset['location'] == input_city, 'loc_clusters']
#     cluster = cluster.iloc[0]
#     # # print(cluster)

#     cities = dataset.loc[dataset['loc_clusters'] == cluster, 'location']
#     # print(cities)
#     # print(len(cities))

#     for c in range(len(cities)):
#       if cities.iloc[c] == input_city:
#         continue
#       else:
#         result.append(cities.iloc[c])
#         # print(cities.iloc[c])
#   except:
#     pass
#   return result