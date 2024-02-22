from django.shortcuts import render
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from v1.core.serializer import AmenitiesSerializer, ConditionSerializer, ImageSerializer, ProductSerializer
from .models import Amenities, Conditions, Product, Image

# from rest_framework.pagination import PageNumberPagination


# class LargeResultsSetPagination(PageNumberPagination):
#     page = 2
#     page_size_query_param = 'page'
#     max_page_size = 10


class ProductApi(ListCreateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.select_related('category')
    # pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        params = self.request.query_params
        q = params.get("q")

        if q:
            queryset = queryset.filter(
                Q(name__icontains=q) | Q(description__icontains=q) | Q(price__icontains=q) |
                Q(category__title__icontains=q) | Q(category__description__icontains=q) | Q(region__icontains=q)
            )

        return queryset


class ProductUpdateDelete(RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class ImageCreateAPi(ListCreateAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


class ImageDetailAPi(RetrieveUpdateDestroyAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


# Product funksiyalari ya'ni qulayliklar va takliflar

class ConditionsAPi(ListCreateAPIView):
    queryset = Conditions.objects.all()
    serializer_class = ConditionSerializer


class ConditionsUpdateDelete(RetrieveUpdateDestroyAPIView):
    queryset = Conditions.objects.all()
    serializer_class = ConditionSerializer


class AmenitiesAPi(ListCreateAPIView):
    queryset = Amenities.objects.all()
    serializer_class = AmenitiesSerializer


class AmenitiesUpdateDelete(RetrieveUpdateDestroyAPIView):
    queryset = Amenities.objects.all()
    serializer_class = AmenitiesSerializer
