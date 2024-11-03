from django import forms
from .models import Book
from .models import Author
from .models import Genre



class BooksForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'publication_year', 'genres', 'price', 'discounted_price']



class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['id', 'name']

    
class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ['name']





##generic form