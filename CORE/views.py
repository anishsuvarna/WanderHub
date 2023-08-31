from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User
import pickle
import pandas as pd
import json
from geopy.exc import GeocoderTimedOut
from geopy.geocoders import Nominatim

# from .utils import getCityList

with open("city_cluster.pkl", "rb") as f:
  city_cluster = pickle.load(f)

with open("restaurant_cluster.pkl", "rb") as f:
  restaurant_cluster = pickle.load(f)

df_city = pd.read_csv("City_with_cluster.csv")
df_restaurant = pd.read_csv("swiggy_with_cluster.csv")
df_places = pd.read_csv('Places.csv')

def findGeocode(city):
    try:
        geolocator = Nominatim(user_agent="WanderHub")
          
        loc = geolocator.geocode(city)
        return loc.latitude, loc.longitude
      
    except GeocoderTimedOut:
          
        return findGeocode(city)

def findDistance(lat1, lon1, lat2, lon2):
  # applying haversine formula.
  dlon = lon2 - lon1
  dlat = lat2 - lat1
  a = (pow(dlat, 2) + pow(dlon, 2) * 0.5)
  c = 2 * 6371 * pow(a, 0.5)
  return c

def hello_world(request):
  return render(request, 'home.html')

def city_search(request):
   return render (request, 'city_search.html')


def get_city_search(request):
  data = request.GET
  city = data.get("search", None)
  latitude, longitude = findGeocode(city)
  print(latitude, longitude)

  val = city_cluster.predict([[latitude, longitude]])[0]

  cities = df_city[df_city["cluster_label"]==val].to_dict('records')
  # places = df_places[df_places['City'] == 'Manali'].to_dict('records')
  # for city in city:
  #   city["Places"] = df_places[df_places['City'] == city['City']].to_dict('records')

  for city in cities:
    # city["List_of_Places"] = df_places[df_places['City'] == city['City']].to_dict('records')
    city["City_desc"] = city["City_desc"].split('.')[0][2:]

  # cities.sort(key=lambda x: x['City'])
  # print(cities)

  return render(request, 'showCities.html', {'cities': cities})

def get_city(request):
  data = request.GET
  print(data)
  latitude = float(data.get("latitude", 0.0))
  longitude = float(data.get("longitude", 0.0))
  print(latitude, longitude)

  val = city_cluster.predict([[latitude, longitude]])[0]

  cities = df_city[df_city["cluster_label"]==val].to_dict('records')
  # places = df_places[df_places['City'] == 'Manali'].to_dict('records')
  # for city in city:
  #   city["Places"] = df_places[df_places['City'] == city['City']].to_dict('records')

  for city in cities:
    # city["List_of_Places"] = df_places[df_places['City'] == city['City']].to_dict('records')
    city["City_desc"] = city["City_desc"].split('.')[0][2:]


  # cities.sort(key=lambda x: x['City'])
  # print(cities)

  return render(request, 'showCities.html', {'cities': cities})

def restauant_search(request):
    return render (request, 'restaurant_search.html')

def get_restaurant_search(request):
  data = request.GET
  data = data.get("search", None)
  if len(data.split(',')) == 2:
    city = data.split(',')[0]
    cuisine = data.split(',')[1]
  else:
    city = data.split(',')[0]
    cuisine = None
  latitude, longitude = findGeocode(city)
  # print(latitude, longitude)

  val = restaurant_cluster.predict([[latitude, longitude]])[0]

  restaurant = df_restaurant[df_restaurant["cluster_label"]==val]
  if cuisine:
    restaurant = restaurant[restaurant["cuisine"].str.lower() == cuisine.lower()]
  restaurant["distance"] = findDistance(latitude, longitude, restaurant["Latitude"], restaurant["Longitude"])
  restaurant = restaurant.sort_values(by=['distance']).to_dict('records')
  # print(restaurant)


  return render(request, 'showRestaurants.html', {'restaurants': restaurant})

def get_restaurant(request):
  data = request.GET
  latitude = float(data.get("latitude", 0.0))
  longitude = float(data.get("longitude", 0.0))
  print(latitude, longitude)

  val = restaurant_cluster.predict([[latitude, longitude]])[0]

  restaurant = df_restaurant[df_restaurant["cluster_label"]==val]
  restaurant["distance"] = findDistance(latitude, longitude, restaurant["Latitude"], restaurant["Longitude"])
  restaurant = restaurant.sort_values(by=['distance']).to_dict('records')
  # print(restaurant)


  return render(request, 'showRestaurants.html', {'restaurants': restaurant})


def login_view(request):
  if request.method != 'POST':
    return render(request, 'regForm.html')
  
  try:
    username = request.POST['username']
    password = request.POST['password']
    user = User.objects.get(username=username)
    if user.check_password(password):
      return redirect('/home/')
    else: 
      return redirect('/login/')
  except User.DoesNotExist:
    return HttpResponse('User does not exist')


def signup(request):
  if request.method != 'POST':
    return HttpResponse('Invalid request')
  password = request.POST['password']
  email = request.POST['email']
  username = request.POST['username']
  user = User.objects.create_user(username=username, password=password, email=email)
  user.save()
  return redirect('/login/')