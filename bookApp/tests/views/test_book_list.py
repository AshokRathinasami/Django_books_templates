import pytest 
from django.test.client import Client
from django.urls import reverse
from pytest_django.asserts import assertRedirects
from bookApp.models import Book, Author, Genre
from django.contrib.auth.models import User, Group, Permission



def test_with_unauthenticated_user():

    # Arange
    url = reverse('books:book_list') 
    client = Client()

    # Act
    response = client.get(url)

    # Assert
    assert response.status_code == 302
    redirect_url = f"{reverse('login')}?next={url}"
    assertRedirects(response, redirect_url)



@pytest.mark.django_db
def test_with_empty_book_list():

    # Arange
    url = reverse('books:book_list') 
    user = User.objects.create_user(username="root", password="password@123")
    client = Client()
    client.login(username="root", password="password@123")

    # Act
    response = client.get(url)

    # Assert
    assert response.status_code == 200
    assert "No books found" in response.content.decode()








