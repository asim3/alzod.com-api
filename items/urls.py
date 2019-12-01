from rest_framework import routers
from .views import ItemViewSet

router = routers.DefaultRouter()
router.register(r'^item', ItemViewSet)

urlpatterns = router.urls