import pytest
from django.test.client import Client
from django.urls import reverse
from pytest_django.asserts import assertRedirects, assertContains
from bookApp.models import Book, Author, Genre
from django.contrib.auth.models import User
from django.contrib.auth.models import User, Group, Permission


@pytest.mark.django_db
def test_book_list_by_author_unauthenticated_user():
    """
    Test that an unauthenticated user is redirected to the login page
    when trying to access the list of books by author.
    """
    # Arrange
    author = Author.objects.create(name="Author 1")
    url = reverse('books:books_by_author', kwargs={'author_id': author.id})
    client = Client()

    # Act
    response = client.get(url)

    # Assert
    assert response.status_code == 302
    redirect_url = f"{reverse('login')}?next={url}"
    assertRedirects(response, redirect_url)


@pytest.mark.django_db
def test_book_list_by_author_authenticated_user_with_empty_list():
    """
    Test that an authenticated user sees the correct message
    when there are no books by the specified author.
    """
    # Arrange
    author = Author.objects.create(name="Author 2")
    user = User.objects.create_user(username="root", password="password@123")
    client = Client()
    client.login(username="root", password="password@123")

    url = reverse('books:books_by_author', kwargs={'author_id': author.id})

    # Act
    response = client.get(url)

    # Assert
    assert response.status_code == 200
    assertContains(response, "No books found")





@pytest.fixture
def create_seller_group(db):
    """Fixture to create a seller group with permissions."""
    seller_group, created = Group.objects.get_or_create(name='seller')
    add_book_permission = Permission.objects.get(codename='add_book')
    change_book_permission = Permission.objects.get(codename='change_book')
    delete_book_permission = Permission.objects.get(codename='delete_book')
    seller_group.permissions.add(add_book_permission, change_book_permission, delete_book_permission)
    return seller_group




@pytest.mark.django_db
def test_create_book_seller(create_seller_group):
    # Arrange
    url = reverse('books:add_book')
    user = User.objects.create_user(username='testSeller', password='password123')
    user.groups.add(create_seller_group)
    client = Client()
    client.login(username='testSeller', password='password123')

    # Create author and genre
    author = Author.objects.create(name="Viramuthu")
    genre = Genre.objects.create(name="Fiction")

    # Act
    response = client.post(url, {
        'title': "Viramuthu's Book",
        'author': author.id,
        'publication_year': 2023,
        'genres': [genre.id],
    })

    # Assert
    assert response.status_code == 302  # Assuming a successful creation redirects
    fetched_book = Book.objects.get(title="Viramuthu's Book")
    assert fetched_book.title == "Viramuthu's Book"
    assert fetched_book.author == author
    assert fetched_book.publication_year == 2023
    assert genre in fetched_book.genres.all()





