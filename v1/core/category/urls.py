from django.urls import path
from .views import CategoryList, CategoryUserAll, CategoryCRUD

urlpatterns = [
    path('category_user/', CategoryUserAll.as_view()),  # urls for user


    path('categorylist_admin/', CategoryList.as_view()),  # url  for admin
    path('category_admin/<int:pk>', CategoryCRUD.as_view()),  # url for admin

]
