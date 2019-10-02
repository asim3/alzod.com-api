from django.urls import include, path
from django.contrib import admin
from django.views.generic import TemplateView
from .routers import router
from members.views import UserLoginView


landing_page = TemplateView.as_view(template_name="index.html")

urlpatterns = [
    path('api/', include(router.urls)),
    path('login/', UserLoginView.as_view()),
    path('admin/', admin.site.urls),
    path('<int:id>', landing_page ),
    path('<int:id>/', landing_page ),
    path('', landing_page ),
]
