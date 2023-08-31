from django.urls import path

from .views import *

app_name = "CORE"

urlpatterns = [
  path('', login_view ,name="indexView"),
  path('login/', login_view ,name="indexView"),
  path('signup/', signup ,name="indexView"),
  path('get_city/', get_city ,name="getCity"),
  path('get_restaurant/', get_restaurant ,name="getRestaurant"),
  path('city_search/', city_search ,name="citySearch"),
  path('restaurant_search/', restauant_search ,name="restauantSearch"),
  path('get_city_search/', get_city_search ,name="getCitySearch"),
  path('get_restaurant_search/', get_restaurant_search ,name="getRestaurantSearch"),
  path('home/', hello_world ,name="loginView"),
]
