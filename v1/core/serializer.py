from .models import Amenities, LikeDislike, Product, Image, Conditions
from rest_framework import serializers


class ConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conditions
        fields = ("id", "title", "amenity")


class AmenitiesSerializer(serializers.ModelSerializer):
    conditions = serializers.SerializerMethodField()

    class Meta:
        model = Amenities
        fields = ("id", "name", 'conditions')

    def get_conditions(self, obj):
        # return ConditionSerializer(obj.amenty_conditions.all(), many=True).data
        return ConditionSerializer(
            Conditions.objects.select_related('amenity').filter(amenity_id=obj.id), many=True
        ).data


class ProductSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
        "id", "region", "name", "description", "price", "price_currency", "status", "category", "amenits", "images")
        extra_kwargs = {"category": {"required": True}}
        extra_kwargs = dict(status=dict(required=True, allow_null=False))

    def get_images(self, obj):
        images = Image.objects.filter(product_id=obj.id).values_list('image')
        return [image[0] for image in images] if images else None

    def to_representation(self, instance):
        res = super().to_representation(instance)
        if res.get('category'):
            res['category'] = {
                "id": instance.category.id,
                "title": instance.category.title,
                "description": instance.category.description
            }
        if res.get('amenits'):
            res['amenits'] = AmenitiesSerializer(instance.amenits.all(), many=True).data
        return res


class ProductLikeDislikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeDislike
        fields = ("id", "like_dislike", "product")

    def create(self, validated_data):
        like_dislike = validated_data.get("like_dislike")
        product = validated_data.get("product")
        like_buttom, _ = LikeDislike.objects.get_or_create(user_id=self.context['request'].user.id,
                                                           product_id=product.id)
        if like_dislike == 1 and like_buttom.like_dislike != True:
            like_buttom.like_dislike = True
            like_buttom.save()
        elif like_buttom == 2 and like_buttom.like_dislike != False:
            like_buttom.like_dislike = False
            like_buttom.save()
        elif like_buttom.like_dislike == 3 and like_buttom.like_dislike != None:
            like_buttom.like_dislike = None
            like_buttom.save()
        return like_buttom

    def to_representation(self, instance):
        return super().to_representation(instance)


class ImageProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ("id", "image")


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ("id", "image", "product")

# class ProductsGetImagesSerializer(serializers.ModelSerializer):
#     product_id = serializers.CharField()

#     class Meta:
#         model = Image
#         fields = ("id", "product_id")


#     def product_get_image(self, obj):
#         product = obj.get("product_id")
#         images = Image.objects.filter(product_id=product.id)
#         return Response({
#             "products_images" : images
#         })
