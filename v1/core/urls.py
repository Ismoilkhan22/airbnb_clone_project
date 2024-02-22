from django.urls import path
from .views import (
    ProductApi,
    ProductUpdateDelete,
    ImageCreateAPi,
    ImageDetailAPi,
    ConditionsAPi,
    AmenitiesAPi,
    ConditionsUpdateDelete,
    AmenitiesUpdateDelete
    )

urlpatterns = [
    path("product/", ProductApi.as_view()),
    path("product/update-delete/<int:pk>/", ProductUpdateDelete.as_view()),
    path("image/", ImageCreateAPi.as_view()),
    path("image/detail/<int:pk>", ImageDetailAPi.as_view()),
    path("conditions/", ConditionsAPi.as_view()),
    path("amenities-condition/", AmenitiesAPi.as_view()),
    path("conditions-udate/<int:pk>/", ConditionsUpdateDelete.as_view()),
    path("amenities-update/<int:pk>/", AmenitiesUpdateDelete.as_view())
]