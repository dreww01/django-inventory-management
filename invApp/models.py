from django.db import models

# Create your models here.
# create a Product class

class Product(models.Model):
    Product_id = models.AutoField(primary_key=True) #primary key = unique id
    name = models.CharField(max_length=100)
    sku = models.CharField(max_length=20, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2) #max digits = 10, decimal places = 2()
    quantity = models.PositiveIntegerField()
    supplier = models.CharField(max_length=100)


    def __str__(self):
        return self.name