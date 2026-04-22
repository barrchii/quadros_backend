from rest_framework import serializers


class AddToCartSerializer(serializers.Serializer):
    slug = serializers.SlugField()
    size = serializers.ChoiceField(choices=['medium', 'large'])
    frame = serializers.ChoiceField(choices=['none', 'black', 'wood'])