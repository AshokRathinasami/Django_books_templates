import decimal
from django.core.management.base import BaseCommand
from bookApp.models import Book

class Command(BaseCommand):
    help = "Apply a discount to all books"

    def add_arguments(self, parser):
        parser.add_argument('discount_percentage', type=int, help="Discount percentage")

    def handle(self, *args, **kwargs):
        discount_percentage = kwargs['discount_percentage'] / 100
        books = Book.objects.all()

        for book in books:
            try:
                # Check if the book has a valid price
                if book.price is None:
                    raise ValueError(f"Book '{book.title}' does not have a price.")

                original_price = book.price
                discount_amount = decimal.Decimal(discount_percentage) * original_price
                discounted_price = original_price - discount_amount

                # Update discounted price and save the book
                book.discounted_price = discounted_price
                book.save()

                self.stdout.write(f"Original Price: {original_price}, Discounted Price: {discounted_price}")

            except ValueError as e:
                # Handle cases where the price is missing or invalid
                self.stdout.write(self.style.ERROR(f"Error: {e}"))

            except Exception as e:
                # Catch any other exceptions
                self.stdout.write(self.style.ERROR(f"An unexpected error occurred for book '{book.title}': {e}"))
