from django.urls import include, path
from django.contrib import admin
from rest_framework import routers

from quickstart import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'modules', views.ModuleViewSet, basename='module')
router.register(r'professors', views.ProfessorViewSet, basename='professor')
router.register(r'ratings', views.RatingViewSet, basename='rating')


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('api/token-login/', views.token_login, name='token-login'),
    path('api/logout/', views.logout),
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('professors/<str:professor_code>/modules/<str:module_code>/', views.professorModuleRatingViewSet.as_view({'get': 'retrieve'}), name='professor-module-rating'),
]