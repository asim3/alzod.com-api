from django.urls import include, path
from django.contrib import admin


urlpatterns = [
  # path('<pk:int>/', include("individual.urls")),
  # path('i/', include("individual.urls")),
  # path('g/', include("group.urls")),
  path('test/', include("items.urls")),
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
