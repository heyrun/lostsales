from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Products(models.Model):
    SUB_CHOICES = [(100, 'HealthPlus'),
                   (200, 'CasaBella')]

    upc = models.CharField(max_length=200)
    alu = models.CharField(max_length=200, null=True, blank=True)
    subsidiary = models.CharField(choices=SUB_CHOICES, max_length=20)
    description = models.CharField(max_length=250)
    attributes = models.CharField(max_length=50, null=True, blank=True)
    size = models.CharField(max_length=50, null=True, blank=True)
    cost = models.FloatField()
    price = models.FloatField()
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = ("Products")
        verbose_name_plural = ("Products")

    def __str__(self):
        return self.description

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    # def get_absolute_url(self):
    #     return reverse("Products_detail", kwargs={"pk": self.pk})


class Region(models.Model):
    region = models.CharField(max_length=200)
    Manager = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.region


class Stores(models.Model):
    SUB_CHOICES = [('100', 'HealthPlus'),
                   ('200', 'CasaBella')]
    name = models.CharField(max_length=200)
    subsidiary = models.CharField(choices=SUB_CHOICES, max_length=20)
    store_code = models.CharField(max_length=5)
    email = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=200, null=True, blank=True)
    region = models.ForeignKey(
        "Region", on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = ("stores")
        verbose_name_plural = ("stores")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("stores_detail", kwargs={"pk": self.pk})


class Lostsales(models.Model):
    user = models.ForeignKey(User,  on_delete=models.CASCADE)
    product = models.ForeignKey(
        'Products', on_delete=models.CASCADE, related_name='product')
    quantity = models.IntegerField(default=1)
    store = models.ForeignKey("Stores", null=True, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now=True)
    # TODO: Define fields here

    class Meta:
        """Meta definition for Lostsales."""

        verbose_name = 'Lostsales'
        verbose_name_plural = 'Lostsales'

    def __str__(self):
        return self.product.description


class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    branch = models.ForeignKey(
        "stores", on_delete=models.SET_NULL, null=True, blank=True)

    # TODO: Define fields here

    class Meta:
        """Meta definition for Staff."""

        verbose_name = 'Staff'
        verbose_name_plural = 'Staff'

    def __str__(self):
        return self.user.username
