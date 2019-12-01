from django.urls import include, path
from django.contrib import admin


urlpatterns = [
  path('f/', include("files.urls")),
  path('content/', include("contents.urls")),
  # path('u/', include("user.urls")),
  # path('g/', include("group.urls")),
  path('token/', include("tokens.urls")),
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
