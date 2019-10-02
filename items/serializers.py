from rest_framework.serializers import HyperlinkedModelSerializer
from .models import Item


class ItemSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Item
        fields = [
            "id", "type", "title", "img", "add_date", "update_date", 
            "description", "price", "country", "currency", 
        ]
