from django.urls import path
from . import views


# where routing is done
urlpatterns = [
    path('', views.place_list, name='place_list'),
    path('place/<int:place_pk>/was_visited', views.place_was_visited, name='place_was_visited'),
    path('about', views.about, name='about'),  # creating an about URL pattern
    path('visited', views.places_visited, name='places_visited'),
    path('place/<int:place_pk>/', views.place_details, name='place_details'),
    path('place/<int:place_pk>/delete', views.delete_place, name='delete_place'),
]