from rest_framework import routers

from authentication.views import SignupViewset

router = routers.SimpleRouter()

router.register('signup', SignupViewset, basename='signup')
