from django.contrib import admin
from django.urls import path, include
from .views import ProjectViewSet, SignupView, TaskViewSet
from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
router = DefaultRouter()
router.register(r'project/crud', ProjectViewSet, basename='projects') # we can also create 4 endpoints for crud operatoins but i prefer one because this is assement
router.register(r'tasks/crud', TaskViewSet, basename='task') # also same for this
urlpatterns = [
    path('', include(router.urls)), # this is calling the above routes 
    path('signup/', SignupView.as_view(), name='signup'), # we can customize the response of view as we needed.
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'), # we should create here custom login
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
