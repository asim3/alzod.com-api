from rest_framework import routers
from members.views import UserViewSet
from items.views import ItemViewSet

router = routers.DefaultRouter()
router.register(r'^user', UserViewSet)
router.register(r'^item', ItemViewSet)

# Members
# path('auth/', "view"),
# path('login/', "view"),
# path('register/', "view"),

# Tasks
# path('tasks/', "view"),
# path('report/', "view"),

# links    
# path('starred/', "view"),
# path('favorite/', "view"),
# path('follow/', "view"),
# path('cart/', "view"),

# Items
# path('new/', "view"),
# path('edit/<int:id>/', "view"),
