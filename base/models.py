from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=50, blank=True)
    email = models.CharField(max_length=100, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



class Tag(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name



class Product(models.Model):

    CATEGORY =(
        ("Indoor", "Indoor"),
        ("Outdoor", "Outdoor")
    )

    name = models.CharField(max_length=100, null=True)
    price = models.FloatField(max_length=200, null=True)
    category = models.CharField(max_length=200, null=True, choices=CATEGORY)
    description = models.TextField(max_length=200, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    tag = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name



class Order(models.Model):

    STATUS = (
        ("Pending", "Pending"),
        ("Out for delivery", "Out for delivery"),
        ("Delivered", "Delivered")
    )

    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.product.name