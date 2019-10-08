from rest_framework import routers
from members.views import AuthUserView
from items.views import ItemViewSet

router = routers.DefaultRouter()
router.register(r'^auth', AuthUserView, basename="auth")
router.register(r'^item', ItemViewSet)

# Members
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
