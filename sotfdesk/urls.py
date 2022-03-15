
from django.contrib import admin
from rest_framework import routers
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

#from project.urls import router as project_router

from authentication.urls import router as auth_router

router = routers.SimpleRouter()
#router.registry.extend(project_router.registry)
router.registry.extend(auth_router.registry)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('api/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include('project.urls')),
    #path('api/', include(router.urls)),

]
