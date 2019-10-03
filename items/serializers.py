from rest_framework.serializers import HyperlinkedModelSerializer, ReadOnlyField
from .models import Item


class ItemSerializer(HyperlinkedModelSerializer):
    read_field = ReadOnlyField(source='title')
    default_field = ReadOnlyField(default='my title')

    class Meta:
        model = Item
        fields = [
            "read_field", "default_field", "type", "title", "img", "country",
            "add_date", "update_date", "description", "price", "currency", 
        ]
