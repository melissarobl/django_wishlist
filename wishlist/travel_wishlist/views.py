from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm, TripReviewForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages


@login_required
# Create your views here.
def place_list(request):
    if request.method == 'POST':
        # create a new place
        form = NewPlaceForm(request.POST) # creating a form from data in the request
        place = form.save(commit=False) # creating a model object from form, get but don't save yet (false)
        place.user = request.user
        if form.is_valid(): # validation against DB constraints
            place.save() # save place to db
            return redirect('place_list')  # reloads home page


    places = Place.objects.filter(user=request.user).filter(visited=False).order_by('name')
    new_place_form = NewPlaceForm()  # used to create HTML
    return render(request, 'travel_wishlist/wishlist.html', {'places': places, 'new_place_form': new_place_form})

@login_required
def places_visited(request):
    # database queried for places that match a particular condition
    visited = Place.objects.filter(visited=True).order_by('name')
    # returns a template and data from the database
    return render(request, 'travel_wishlist/visited.html', {'visited': visited})


@login_required
def place_was_visited(request, place_pk):
    if request.method == 'POST':
        # place = Place.objects.get(pk=place_pk) # database query that matches this query
        place = get_object_or_404(Place, pk=place_pk) # if not found, 404 error is returned
        if place.user == request.user:
            place.visited = True
            place.save()
        else:
            return HttpResponseForbidden()

    return redirect('place_list')
    # return redirect ('places_visited) # if you want to go to places visited page after clicking button 'visited'


@login_required
def about(request):
    author = 'Melissa'
    about = 'A website to create a list of places to visit'
    return render(request, 'travel_wishlist/about.html', {'author': author, 'about': about})


@login_required
def place_details(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)

    # does this place belong to the current user?
    if place.user != request.user:
        return HttpResponseForbidden()
    # Put in data the user sent. Use that to update model instance in database.
    # if POST, validate form data and update
    if request.method == 'POST':
        form = TripReviewForm(request.POST, request.FILES, instance=place) # make a trip review form object from data sent with HTTP request.
        if form.is_valid():
            form.save()
            messages.info(request, 'Trip information updated!')
        else:
            messages.error(request, form.errors) # temporary , refine later

        return redirect('place_details', place_pk)

    else:  # GET or POST request? If GET --> show Place info and optional form / form If place is visited, show form; if place is not visited, no form
        if place.visited:
            review_form = TripReviewForm(instance=place)
            return render(request, 'travel_wishlist/place_detail.html', {'place': place, 'review_form': review_form})
        else:
            return render(request, 'travel_wishlist/place_detail.html', {'place': place})


@login_required
def delete_place(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)
    if place.user == request.user:
        place.delete()
        return redirect('place_list')
    else:
        return HttpResponseForbidden()
