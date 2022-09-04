from django import forms
import datetime
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import Suggestion,Book


class SuggestionForm(forms.ModelForm):
    class Meta:
        model = Suggestion
        fields = ('BookTitle','Category','ISBN')

        widgets = {
            'BookTitle':forms.TextInput(attrs={'class':'form-control'}),
            'Category':forms.TextInput(attrs={'class':'form-control'}),
            'ISBN':forms.TextInput(attrs={'class':'form-control'}),

        }
        labels = {
            'BookTitle': 'Title',
            'Category': 'Category',
            'ISBN':'ISBN/DOIN'
        }

BookDropdown = [('booktitle','Book Title'),('category','Category'),('isbn','ISBN')]
# ,('author','Author'
BOOK_CHOICES = (
        ('Book', 'Book'),
        ('Journal', 'Journal'),
        ('Thesis', 'Thesis'),

    )
class TypeSearchForm(forms.Form):

    Search_type = forms.CharField(label = '   What do you want to search',widget = forms.Select(attrs={ 'class':'form-control col','style':  'margin:50px',  },choices=BOOK_CHOICES))


class BookSearchForm(forms.Form):

    Search_for = forms.CharField( widget=forms.TextInput(attrs={'placeholder': 'Search for','class':'form-control'})) #'style':  'margin-left:30px;margin-right:30px; margin-top:40px; margin-bottom:40px; ', 'class': ' center form-control col'}
   # Select = forms.CharField(widget=forms.RadioSelect(choices=BOOK_CHOICES,attrs={'style':  'size = 20 ;margin:50px; margin-top:40px; margin-bottom:40px;','class':' form-control '}))
    Select = forms.ChoiceField(label = "Select",choices=BOOK_CHOICES,widget=forms.RadioSelect(attrs={'class':'form-check-inline'}))

    Search_by = forms.CharField(label = 'Search by ',widget = forms.Select(attrs={ 'style':  'size = 20 ;width:100px;margin-left:40px;margin-right:40px; margin-top:40px; margin-bottom:40px;','class':'dropdown form-control col' },choices=BookDropdown))
    
    