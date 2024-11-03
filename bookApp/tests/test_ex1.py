from django.test import TestCase,Client
from django.urls import reverse
from bookApp.models import Book, Author, Genre
from django.contrib.auth.models import User, Group, Permission
from django.core.management import call_command
from decimal import Decimal
import pytest






@pytest.fixture
def create_seller_group(db):
    """Fixture to create a seller group with permissions."""
    seller_group, created = Group.objects.get_or_create(name='seller')
    add_book_permission = Permission.objects.get(codename='add_book')
    change_book_permission = Permission.objects.get(codename='change_book')
    delete_book_permission = Permission.objects.get(codename='delete_book')
    seller_group.permissions.add(add_book_permission, change_book_permission, delete_book_permission)
    return seller_group


@pytest.fixture
def create_buyer_group(db):
    """Fixture to create a buyer group with permissions."""
    buyer_group, created = Group.objects.get_or_create(name='buyer')
    view_book_permission = Permission.objects.get(codename='view_book')
    buyer_group.permissions.add(view_book_permission)
    return buyer_group


@pytest.fixture
def create_author_and_genres(db):
    """Fixture to create test data for authors and genres."""
    author = Author.objects.create(name="Viramuthu")
    genre1 = Genre.objects.create(name="Fiction")
    genre2 = Genre.objects.create(name="Adventure")
    return author, genre1, genre2


@pytest.mark.django_db
def test_create_book(client: Client, create_seller_group):
    # Create user and assign to seller group
    user = User.objects.create_user(username='testSeller', password='password123')
    user.groups.add(create_seller_group)

    # Login the user
    client.login(username='testSeller', password='password123')


    # Create author and genre
    author = Author.objects.create(name="Viramuthu")
    genre = Genre.objects.create(name="Fiction")

    # Create book
    book = Book.objects.create(title="Viramuthu's Book", author=author, publication_year=2023)
    book.genres.add(genre)

    # Fetch and assert
    fetched_book = Book.objects.get(id=book.id)
    assert fetched_book.title == "Viramuthu's Book"
    assert fetched_book.author == author
    assert fetched_book.publication_year == 2023
    assert genre in fetched_book.genres.all()
