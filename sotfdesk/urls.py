
from django.contrib import admin
from rest_framework import routers
from django.urls import path, include


from project.urls import router as project_router
from authentication.urls import router as auth_router

router = routers.SimpleRouter()
router.registry.extend(project_router.registry)
router.registry.extend(auth_router.registry)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls)),

]
