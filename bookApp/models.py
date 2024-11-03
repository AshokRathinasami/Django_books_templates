from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return (f"{self.name}")
    
class Book(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=20)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    publication_year = models.IntegerField()
    genres = models.ManyToManyField(Genre)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"ID: {self.id}, Title: {self.title}, Author ID: {self.author}, Publication Year: {self.publication_year}, Genres:{self.genres}, price:{self.price}"
        # return (f"{self.title}{self.author_id}{self.publication_year}")

    def book_details(self):
        return (f"title{self.title,self.author.name}")
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    biodata = models.TextField()

    def __str__(self):
        return self.user.username
    
