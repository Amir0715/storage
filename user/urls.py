from user import views
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', views.UsersViewSet, basename='users')
router.register(r'private/users', views.AdminViewSet, basename='admin')
router.register(r'auth', views.AuthViewSet, basename='auth')

urlpatterns = [
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('', SpectacularSwaggerView.as_view(url_name='schema'),
         name='swagger-ui'),
    path('', include(router.urls)),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]