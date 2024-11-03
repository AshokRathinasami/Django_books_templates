from django.contrib import admin
from .models import Book, Author, Genre, Profile

# Custom admin for Author model
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Display the name field in the list view
    search_fields = ('name',)  # Add a search box for the name field

# Custom admin for Genre model
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Display the name field in the list view
    search_fields = ('name',)  # Add a search box for the name field

# Custom admin for Book model
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year', 'price', 'discounted_price')  # Display fields in list view
    list_filter = ('author', 'genres', 'publication_year')  # Add filter options
    search_fields = ('title', 'author__name')  # Add a search box for title and author
    filter_horizontal = ('genres',)  # Display genres with horizontal filter for M2M relation
    fieldsets = (
        (None, {
            'fields': ('title', 'author', 'publication_year', 'price', 'discounted_price')
        }),
        ('Genres', {
            'fields': ('genres',)
        }),
    )  # Organize fields into sections

# Register the custom admin forms
admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Genre, GenreAdmin)

admin.site.register(Profile)
