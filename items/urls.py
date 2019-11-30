from rest_framework import routers
from .views import ItemViewSet

items_router = routers.DefaultRouter()
items_router.register(r'^item', ItemViewSet)


