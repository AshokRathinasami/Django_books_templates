import pytest
from django.test.client import Client
from django.urls import reverse
from pytest_django.asserts import assertRedirects, assertContains
from bookApp.models import Book, Author, Genre
from django.contrib.auth.models import User
from django.contrib.auth.models import User, Group, Permission


@pytest.mark.django_db
def test_create_book_unauthenticated():
    
    # Arrange
    url = reverse('books:add_book')
    client = Client()

    # Act
    response = client.get(url)

    # Assert
    assert response.status_code == 302  # Redirect status code
    redirect_url = f"{reverse('login')}?next={url}"  # Expected redirection to login page
    assertRedirects(response, redirect_url)

    # Optionally: Try posting to add_book and check redirect
    response_post = client.post(url, {
        'title': "Test Book",
        'author': 1,  # Using arbitrary author ID for the post attempt
        'publication_year': 2023,
        'genres': [1],  # Using arbitrary genre ID
    })
    assert response_post.status_code == 302
    assertRedirects(response_post, redirect_url)



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
    assert response.status_code == 302  
    fetched_book = Book.objects.get(title="Viramuthu's Book")
    assert fetched_book.title == "Viramuthu's Book"
    assert fetched_book.author == author
    assert fetched_book.publication_year == 2023
    assert genre in fetched_book.genres.all()



@pytest.mark.django_db
def test_create_book_with_empty_fileds(create_seller_group):
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
        'title': "",
        'author': "",
        'publication_year': "",
        'genres': "",
    })

    # Assert
    assert response.status_code == 200

    # Check that each field has the expected error
    assert "title" in response.context["form"].errors
    assert response.context["form"].errors["title"] == ["This field is required."]
    
    assert "author" in response.context["form"].errors
    assert response.context["form"].errors["author"] == ["This field is required."]
    
    assert "publication_year" in response.context["form"].errors
    assert response.context["form"].errors["publication_year"] == ["This field is required."]
    
    assert "genres" in response.context["form"].errors
    assert response.context["form"].errors["genres"] == ["“” is not a valid value."]





@pytest.mark.django_db
def test_create_book_with_invalid_fileds(create_seller_group):
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
        'title': "asjnjnjskakala12212121",      # more than 20 characters
        'author': "ascdededed",                 # Invalid author format
        'publication_year': "abcdss",           # Invalid year format (should be a number)
        'genres': "noooooo",                    # Invalid genre
    })

    # Assert
    assert response.status_code == 200

   
    assert "title" in response.context["form"].errors
    assert response.context["form"].errors["title"] == [
        "Ensure this value has at most 20 characters (it has 22)."
    ]
    
    assert "author" in response.context["form"].errors
    assert response.context["form"].errors["author"] == ["Select a valid choice. That choice is not one of the available choices."]
    
    assert "publication_year" in response.context["form"].errors
    assert response.context["form"].errors["publication_year"] == ["Enter a whole number."]
    
    assert "genres" in response.context["form"].errors
    assert response.context["form"].errors["genres"] == ['“noooooo” is not a valid value.']







@pytest.mark.django_db
def test_create_book_with_non_exist_author_filed(create_seller_group):
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
        'author': "viram",
        'publication_year': 2023,
        'genres': [genre.id],
    })


    # Assert
    assert response.status_code == 200
    
    assert "author" in response.context["form"].errors
    assert response.context["form"].errors["author"] == ["Select a valid choice. That choice is not one of the available choices."]
    





@pytest.mark.django_db
def test_create_book_with_non_exist_gener_filed(create_seller_group):
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
        'genres': "abcd",
    })


    # Assert
    assert response.status_code == 200
    
    assert "genres" in response.context["form"].errors
    assert response.context["form"].errors["genres"] == ['“abcd” is not a valid value.']



@pytest.mark.django_db
def test_create_book_seller_with_optinal_fileds(create_seller_group):
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
        'price' : 200
    })

    # Assert
    assert response.status_code == 302  
    fetched_book = Book.objects.get(title="Viramuthu's Book")
    assert fetched_book.title == "Viramuthu's Book"
    assert fetched_book.author == author
    assert fetched_book.publication_year == 2023
    assert genre in fetched_book.genres.all()
    assert fetched_book.price == 200








@pytest.mark.django_db
@pytest.mark.parametrize(
    "title, publication_year, price",
    [
        ("Viramuthu's Book", 2023, 200),  # With price
        ("Viramuthu's Book 2", 2022, None),  # Without price
       
    ]
)
def test_create_book_seller_with_optional_fields_using_parametrized(
    create_seller_group, title, publication_year, price
):
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
    data = {
        'title': title,
        'author': author.id,
        'publication_year': publication_year,
        'genres': [genre.id],
    }


    response = client.post(url, data)

    # Assert
    assert response.status_code == 302 
    fetched_book = Book.objects.get(title=title)
    assert fetched_book.title == title
    assert fetched_book.author == author
    assert fetched_book.publication_year == publication_year
    assert genre in fetched_book.genres.all()







# assert "other_location" in response.context["form"].errors
#     assert response.context["form"].errors["other_location"] == [
#         "Please provide the other location."
#     ]




#   def test_with_empty_fields():
# 	# all empty
# 	data = {
# 		'title': '',
# 		'author': '',
# 		'publication_year': '',
# 		'genres': '',
# 		'price': '',
# 		'discounted_price': ''
# 	}


# def test_with_invalid_values():
# 	# not-null but invalid
# 	data = {
# 		'title': 'hi',
# 		'author': 'hello',
# 		'publication_year': 'acbc',

# 	}

# def test_with_non_existent_author():
# 	# valid data-types but non-existent data
# 	data = {
# 		'title': "Hello World",
# 		'author': 1001,
# 	}

# 	response.context['form'].errors['author'] = ['Error message here']


# def test_with_non_existent_genre():
# 	pass


# def test_happy_path_without_optional_fields():
# 	pass


# def test_happy_path_with_optional_fields():
# 	pass