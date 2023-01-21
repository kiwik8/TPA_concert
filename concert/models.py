from django.db import models

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=100)
    stripe_product_id = models.CharField(max_length=100)
    stock = models.IntegerField(default=100)

    def __str__(self):
        return self.name

class Price(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    stripe_price_id = models.CharField(max_length=100)
    price = models.IntegerField(default=0)


class Client(models.Model):
    email = models.EmailField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        name = self.email.split("@")[0]
        return name + " " + str(self.date)

class Question(models.Model):
    fisrt_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.fisrt_name + " " + self.last_name