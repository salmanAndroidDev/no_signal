from rest_framework import serializers
from .models import Content


class ItemRelatedField(serializers.RelatedField):
    """
        Custom related fields that render items
    """

    def to_representation(self, value):
        return value.render()


class ContentSerializer(serializers.ModelSerializer):
    """
        Model serializer that returns contents and it's rendered item
    """
    item = ItemRelatedField(read_only=True)

    class Meta:
        model = Content
        fields = ('order', 'item')
