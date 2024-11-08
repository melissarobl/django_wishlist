from django import forms
from .models import Place

class NewPlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ('name', 'visited')

class DateInput(forms.DateInput): # create from Django input
    input_type = 'date'

class TripReviewForm(forms.ModelForm): # show what form is the model related to
    class Meta:
        model = Place
        fields = ('notes', 'date_visited', 'photo')
        widgets = {
            'date_visited': DateInput()  # customize the date input created
        }