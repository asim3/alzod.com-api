from django.urls import include, path
from django.contrib import admin
from items.urls import items_router 
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView,TokenVerifyView
from .register import register_view

urlpatterns = [
  # path('<pk:int>/', include(individual_router.urls)),
  # path('i/', include(individual_router.urls)),
  # path('g/', include(group_router.urls)),
  path('t/', include(items_router.urls)),
  path('token/', TokenObtainPairView.as_view(), name='token_obtain'),
  path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
  path('register/', register_view, name='register'),
  path('admin/', admin.site.urls),
]


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
