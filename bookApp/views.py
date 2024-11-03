from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from bookApp.models import Book, Author, Genre
from .forms import BooksForm, AuthorForm, GenreForm


class BookListView(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'bookApp/book_list.html'
    context_object_name = 'books'
    login_url = reverse_lazy('login')


class AuthorListView(LoginRequiredMixin, ListView):
    model = Author
    template_name = 'bookApp/author_list.html'
    context_object_name = 'authors'
    login_url = reverse_lazy('login')


class BookCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Book
    form_class = BooksForm
    template_name = 'bookApp/add_books.html'
    success_url = reverse_lazy('books:book_list')
    permission_required = 'bookApp.add_book'
    login_url = reverse_lazy('login')


class AuthorCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Author
    form_class = AuthorForm
    template_name = 'bookApp/add_author.html'
    success_url = reverse_lazy('books:book_list')
    permission_required = 'bookApp.add_author'
    login_url = reverse_lazy('login')


class GenreCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Genre
    form_class = GenreForm
    template_name = 'bookApp/add_genre.html'
    success_url = reverse_lazy('books:book_list')
    permission_required = 'bookApp.add_genre'
    login_url = reverse_lazy('login')


class BookUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Book
    form_class = BooksForm
    template_name = 'bookApp/update_book.html'
    success_url = reverse_lazy('books:book_list')
    permission_required = 'bookApp.change_book'
    login_url = reverse_lazy('login')

    def get_object(self):
        book_id = self.kwargs.get(self.pk_url_kwarg)
        return get_object_or_404(Book, id=book_id)


class BookDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Book
    template_name = 'bookApp/delete_book.html'
    success_url = reverse_lazy('books:book_list')
    permission_required = 'bookApp.delete_book'
    login_url = reverse_lazy('login')

    def get_object(self):
        book_id = self.kwargs.get(self.pk_url_kwarg)
        return get_object_or_404(Book, id=book_id)


class BookByAuthorListView(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'bookApp/list_of_book_by_author.html'
    context_object_name = 'books'
    login_url = reverse_lazy('login')

    def get_queryset(self):
        author_id = self.kwargs.get('author_id')
        return Book.objects.filter(author_id=author_id)


class BookByGenreListView(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'bookApp/list_of_book_by_genre.html'
    context_object_name = 'books'
    login_url = reverse_lazy('login')

    def get_queryset(self):
        genre_name = self.kwargs.get('genre_name')
        return Book.objects.filter(genres__name=genre_name).distinct()


class BookByPublicationYearView(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'bookApp/list_of_book_by_year.html'
    context_object_name = 'books'
    login_url = reverse_lazy('login')

    def get_queryset(self):
        year = self.kwargs.get('year')
        return Book.objects.filter(publication_year=year)
