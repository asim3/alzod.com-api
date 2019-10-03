from rest_framework.serializers import HyperlinkedModelSerializer, ReadOnlyField
from .models import Item


class ItemSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Item
        fields = [
            "type", "title", "img", "country", "description", 
            "price", "currency",
        ]
        read_only_fields = ["add_date", "update_date", ]

