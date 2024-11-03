from django.test import TestCase
from django.urls import reverse
from bookApp.models import Book, Author, Genre
from django.contrib.auth.models import User, Group, Permission
from django.core.management import call_command
from decimal import Decimal



class BookAppListViewTests(TestCase):


## Testing to list the book with group and users---------

   def test_book_list_view_with_seller_group(self):
        # Step-1 >> Create the 'seller' group and assign permissions
        seller_group, created = Group.objects.get_or_create(name='seller')
        add_book_permission = Permission.objects.get(codename='add_book')
        change_book_permission = Permission.objects.get(codename='change_book')
        delete_book_permission = Permission.objects.get(codename='delete_book')
        seller_group.permissions.add(add_book_permission, change_book_permission, delete_book_permission)

        # Step-2 >> Create new user, add them to the 'seller' group
        user = User.objects.create_user(username='testSeller', password='password123')
        user.groups.add(seller_group)

        # Step-3 >> Login 
        self.client.login(username='testSeller', password='password123')

        # Step-4 >> Create test data (Author, Genre, Book)
        author = Author.objects.create(name="viramuthu")
        genre1 = Genre.objects.create(name="Fiction")
        genre2 = Genre.objects.create(name="Adventure")
        book = Book.objects.create(title="Book1", author=author, publication_year=2023)
        book.genres.add(genre1, genre2)

        # Step-5 >> Test the book list
        response = self.client.get(reverse('books:book_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookApp/book_list.html')
        self.assertContains(response, book.title)
        self.assertContains(response, genre1.name)
        self.assertContains(response, genre2.name)






   def test_book_list_view_with_buyer_group(self):
        # Step 1: Create the 'buyer' group and assign view_book permission
        buyer_group, created = Group.objects.get_or_create(name='buyer')
        view_book_permission = Permission.objects.get(codename='view_book')
        buyer_group.permissions.add(view_book_permission)

        # Step 2: Create new user  add them to the 'buyer' group
        user = User.objects.create_user(username='testBuyer', password='password123')
        user.groups.add(buyer_group)

        # Step 3: Log the user in
        self.client.login(username='testBuyer', password='password123')

        # Step 4: Create test data (Author, Genre, Book)
        author = Author.objects.create(name="viramuthu")
        genre1 = Genre.objects.create(name="Fiction")
        genre2 = Genre.objects.create(name="Adventure")
        book = Book.objects.create(title="Book1", author=author, publication_year=2023)
        book.genres.add(genre1, genre2)

        # Step 5: Test the book list view
        response = self.client.get(reverse('books:book_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookApp/book_list.html')
        self.assertContains(response, book.title)
        self.assertContains(response, genre1.name)
        self.assertContains(response, genre2.name)






## Testing to create the book --------------
    
   def test_create_book(self):
        # Step-1 >> Create the 'seller' group and assign permissions
        seller_group, created = Group.objects.get_or_create(name='seller')
        add_book_permission = Permission.objects.get(codename='add_book')
        change_book_permission = Permission.objects.get(codename='change_book')
        delete_book_permission = Permission.objects.get(codename='delete_book')
        seller_group.permissions.add(add_book_permission, change_book_permission, delete_book_permission)

        # Step-2 >> Create new user, add them to the 'seller' group
        user = User.objects.create_user(username='testSeller', password='password123')
        user.groups.add(seller_group)

        # Step-3 >> Login 
        self.client.login(username='testSeller', password='password123')

        # Create data
        author = Author.objects.create(name="viramuthu")
        genre = Genre.objects.create(name="Fiction")

        # Create book
        book = Book.objects.create(
            title="viramuthu's Book",author=author,
            publication_year=2023
        )
        book.genres.add(genre)

        # Fetch book from the database
        fetched_book = Book.objects.get(id=book.id)

        # Perform assertions
        self.assertEqual(fetched_book.title, "viramuthu's Book")
        self.assertEqual(fetched_book.author, author)
        self.assertEqual(fetched_book.publication_year, 2023)
        self.assertIn(genre, fetched_book.genres.all())


    
 ## Testing to update the book ---------------
  
 
   def test_update_book(self):

        # Step-1 >> Create the 'seller' group and assign permissions
        seller_group, created = Group.objects.get_or_create(name='seller')
        add_book_permission = Permission.objects.get(codename='add_book')
        change_book_permission = Permission.objects.get(codename='change_book')
        delete_book_permission = Permission.objects.get(codename='delete_book')
        seller_group.permissions.add(add_book_permission, change_book_permission, delete_book_permission)

        # Step-2 >> Create new user, add them to the 'seller' group
        user = User.objects.create_user(username='test_seller', password='password123')
        user.groups.add(seller_group)

        # Step-3 >> Login 
        self.client.login(username='test_seller', password='password123')
        # Create data
        author = Author.objects.create(name="viramuthu")
        genre = Genre.objects.create(name="fiction")

        # Create book
        book = Book.objects.create(
            title="Old book",
            author=author,
            publication_year=2023
        )
        book.genres.add(genre)

        # Update book
        book.title = "Updated new book"
        book.publication_year = 2024
        book.save()

        # Fetch book from the database
        updated_book = Book.objects.get(id=book.id)

        #  assertions
        self.assertEqual(updated_book.title, "Updated new book")
        self.assertEqual(updated_book.publication_year, 2024)
        self.assertIn(genre, updated_book.genres.all())




 ## Testing to delete the book ---------------


   def test_delete_book(self):
        
        # Step-1 >> Create the 'seller' group and assign permissions
        seller_group, created = Group.objects.get_or_create(name='seller')
        add_book_permission = Permission.objects.get(codename='add_book')
        change_book_permission = Permission.objects.get(codename='change_book')
        delete_book_permission = Permission.objects.get(codename='delete_book')
        seller_group.permissions.add(add_book_permission, change_book_permission, delete_book_permission)

        # Step-2 >> Create new user, add them to the 'seller' group
        user = User.objects.create_user(username='test_seller', password='password123')
        user.groups.add(seller_group)

        # Step-3 >> Login 
        self.client.login(username='test_seller', password='password123')


        # Create test data
        author = Author.objects.create(name="Author")
        genre = Genre.objects.create(name="fiction")

        # Create and delete a book
        book = Book.objects.create(
            title="Test Book",
            author=author,
            publication_year=2023
        )
        book.genres.add(genre)
        book_id = book.id
        book.delete()

        # Perform assertions
        with self.assertRaises(Book.DoesNotExist):
            Book.objects.get(id=book_id)



### negative scenarios


   def test_book_list_view_without_login(self):
      response = self.client.get(reverse('books:book_list'))
      self.assertEqual(response.status_code, 302)  # Redirect to login
      self.assertRedirects(response, '/accounts/login/?next=/bookApp/')



   def test_create_book_without_permission(self):
    # Create a user without the 'seller' group
    user = User.objects.create_user(username='testUser', password='password123')
    self.client.login(username='testUser', password='password123')

    # Try to access create book view
    response = self.client.get(reverse('books:add_book'))
    self.assertEqual(response.status_code, 403)  


  

   def test_delete_book_without_permission(self):
    # Create a user without the 'seller' group
    user = User.objects.create_user(username='testUser', password='password123')
    self.client.login(username='testUser', password='password123')

    # Create a book
    author = Author.objects.create(name="Author")
    genre = Genre.objects.create(name="Fiction")
    book = Book.objects.create(title="Test Book", author=author, publication_year=2023)
    book.genres.add(genre)

    # Try to delete the book without permission
    response = self.client.post(reverse('books:delete_book', args=[book.id]))
    self.assertEqual(response.status_code, 403)  








class DiscountCommandTests(TestCase):

    def setUp(self):
        # Step-1 >> Create the 'seller' group and assign permissions
        seller_group, created = Group.objects.get_or_create(name='seller')
        add_book_permission = Permission.objects.get(codename='add_book')
        change_book_permission = Permission.objects.get(codename='change_book')
        delete_book_permission = Permission.objects.get(codename='delete_book')
        seller_group.permissions.add(add_book_permission, change_book_permission, delete_book_permission)

        # Step-2 >> Create new user, add them to the 'seller' group
        self.user = User.objects.create_user(username='testSeller', password='password123')
        self.user.groups.add(seller_group)

        # Step-3 >> Create data
        self.author = Author.objects.create(name="Viramuthu")
        self.genre = Genre.objects.create(name="Fiction")

        # Step-4 >> Create book with a price
        self.book = Book.objects.create(
            title="Viramuthu's Book",
            author=self.author,
            price=Decimal('100.00'),  # Assuming price field is DecimalField
            publication_year=2024
        )
        self.book.genres.add(self.genre)

    def test_discount_command(self):
        # Apply a 10% discount using the management command
        call_command('price_command', 10)

        # Fetch the book from the database again to check the updated discount price
        updated_book = Book.objects.get(id=self.book.id)

        # Calculate expected discounted price
        expected_discounted_price = Decimal('100.00') - (Decimal('100.00') * Decimal('0.10'))

        # Assert the discounted price is updated correctly
        self.assertEqual(updated_book.discounted_price, expected_discounted_price)

    def test_discount_command_with_zero_discount(self):
        # Apply a 0% discount
        call_command('price_command', 0)

        # Fetch the book from the database again
        updated_book = Book.objects.get(id=self.book.id)

        # Assert the price remains unchanged (no discount applied)
        self.assertEqual(updated_book.discounted_price, Decimal('100.00'))

   
    def test_discount_command_with_missing_price(self):
        # Create a book without a price
        book_without_price = Book.objects.create(
            title="Book without Price", author=self.author, publication_year=2023
        )
        book_without_price.genres.add(self.genre)

        # Apply a 10% discount
        call_command('price_command', 10)

        # Fetch the book from the database again
        updated_book = Book.objects.get(id=book_without_price.id)

        # Assert that discounted price is still None because price was not set
        self.assertIsNone(updated_book.discounted_price)







