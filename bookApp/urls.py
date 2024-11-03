from django.urls import path

from .views import BookListView,BookCreateView,AuthorCreateView,GenreCreateView,BookUpdateView,BookDeleteView,BookByAuthorListView,AuthorListView,BookByGenreListView,BookByPublicationYearView


app_name = "books"

urlpatterns = [
     path('', BookListView.as_view(), name='book_list'),


     path('createBook/', BookCreateView.as_view(), name='add_book'),
     path('createBookAuthor/', AuthorCreateView.as_view(), name='add_author'),
     path('createBookGenre/', GenreCreateView.as_view(), name='add_genre'),

     path('update/<int:pk>/', BookUpdateView.as_view(), name='update_book'),
     path('delete/<int:pk>/', BookDeleteView.as_view(), name='delete_book'),


     path('authors', AuthorListView.as_view(), name='author_list'),

     path('author/<int:author_id>/', BookByAuthorListView.as_view(), name='books_by_author'),

     path('genre/<str:genre_name>/', BookByGenreListView.as_view(), name='books_by_genre'),
     path('year/<int:year>/', BookByPublicationYearView.as_view(), name='books_by_year'),
]

