from django.urls import include, path
from django.contrib import admin
from django.views.generic import TemplateView
from .routers import router
from members.views import AuthUserView, UserLoginView, UserLogoutView


landing_page = TemplateView.as_view(template_name="index.html")

urlpatterns = [
    path('api/', include(router.urls)),
    
    path('login/', UserLoginView.as_view()),
    path('logout/', UserLogoutView.as_view()),

    path('admin/', admin.site.urls),

    # delete path('user/', landing_page ),

    # landing page
    path('user/<int:id>', landing_page ), 
    path('user/<int:id>/', landing_page ),
    path('<int:id>', landing_page ), 
    path('<int:id>/', landing_page ),
    path('', landing_page ),
]
