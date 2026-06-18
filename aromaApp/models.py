from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    def __str__(self):
        return self.username
class Restuarant(models.Model):
    restuarant_name = models.CharField(max_length=40)
    location = models.CharField(max_length=50)
    cuisine = models.CharField(max_length=50)
    rating = models.FloatField()
    picture = models.URLField(max_length=200,default="https://m.media-amazon.com/images/I/71mlk+5TszL._AC_UF894,1000_QL80_.jpg")
    def __str__(self):
        return self.restuarant_name
class Items(models.Model):
    restuarant = models.ForeignKey(Restuarant,on_delete = models.CASCADE,related_name='items')
    name = models.CharField(max_length = 20)
    description = models.CharField(max_length = 200)
    price = models.FloatField()
    vegeterian = models.BooleanField(default=False)
    picture = models.URLField(max_length = 400, default='https://www.indiafilings.com/learn/wp-content/uploads/2024/08/How-to-Start-Food-Business.jpg')
    def __str__(self):
        return self.name
class Cart(models.Model):
    customer = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "cart")
    items = models.ManyToManyField("Items", related_name = "carts")

    def total_price(self):
        return sum(item.price for item in self.items.all())