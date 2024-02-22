from django.http import Http404
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, GenericAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from v1.core.category.models import Category
from v1.core.category.serializers import CategorySerializers


class CategoryUserAll(GenericAPIView):
    """
    List all categories for users
    """
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializers
    permission_classes = (AllowAny,)

    def get(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class CategoryList(ListCreateAPIView):
    """
    List all categories or create a new category
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializers
    permission_classes = (IsAdminUser,)


class CategoryCRUD(RetrieveUpdateDestroyAPIView):
    """
     update or delete a category ,get
    """
    lookup_field = "pk"
    queryset = Category.objects.all()
    serializer_class = CategorySerializers
    permission_classes = (IsAdminUser,)
