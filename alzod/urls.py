from django.views.generic import TemplateView
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Members
    # path('auth/', AuthorizationView.as_view() ),
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

    # Base
    path('search/', TemplateView.as_view(template_name="base/search.json") ),
    # path('search/', "view"),
    path('<int:id>', TemplateView.as_view(template_name="base/index.html") ),
    path('', TemplateView.as_view(template_name="base/index.html") ),
]
