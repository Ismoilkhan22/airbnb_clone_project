from django.db import models

from registration.models import User
from v1.core.category import Category


class DefaultAbstract(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Amenities(DefaultAbstract):
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name = "Qulaylik"
        verbose_name_plural = "Qulayliklar"

    def __str__(self) -> str:
        return f"{self.name}"


class Conditions(DefaultAbstract):
    amenity = models.ForeignKey(Amenities, on_delete=models.CASCADE, related_name='amenty_conditions')
    title = models.CharField(max_length=200)

    class Meta:
        verbose_name = "Sharoit"
        verbose_name_plural = "Sharoitlar "

    def __str__(self) -> str:
        return self.title


class Product(DefaultAbstract):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    region = models.CharField(max_length=150)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    price = models.IntegerField(verbose_name=200)
    price_currency = models.CharField(max_length=200)
    status = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    amenits = models.ManyToManyField(Amenities)

    def __str__(self) -> str:
        return f"{self.name} - {self.description}"

    def get_image(self):
        return Image.objects.select_related("product").filter(product_id=self.id).first()

    class Meta:
        verbose_name = "Mahsulot"
        verbose_name_plural = "Mahsulotlar"


class Image(DefaultAbstract):
    image = models.ImageField(upload_to="image/")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.image

    class Meta:
        verbose_name = "Rasm"
        verbose_name_plural = "Rasmlar"


class LikeDislike(DefaultAbstract):
    like_dislike = models.BooleanField(default=None)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
