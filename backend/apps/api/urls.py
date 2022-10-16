from pprint import pprint

from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from apps.api import views

router = routers.DefaultRouter()
router.register(r'car', views.CarAPIViewSet, basename='car')
router.register(r'brand', views.CarBrandAPIViewSet, basename='brand')
router.register(r'user', views.UserAPIViewSet, basename='user')
router.register(r'car_doc', views.CarDocumentAPIViewSet, basename='car_doc')
router.register(r'user_doc', views.UserDocumentAPIViewSet, basename='user_doc')
router.register(r'doc_type', views.DocumentTypesAPIViewSet, basename='docs_type')
router.register(r'repair', views.RepairRequestAPIViewSet, basename='repairs')
router.register(r'cards', views.RepairRequestAPIViewSet, basename='cards')

urlpatterns = router.urls

urlpatterns += [
    path('api-token-auth/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api-token-auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api-token-auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]

# pprint(router.urls)