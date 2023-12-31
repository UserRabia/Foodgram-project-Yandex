from rest_framework import routers
from django.urls import path, include

from api.views import TagViewSet, RecipeViewSet, IngredientViewSet, UserViewSet

routers = routers.DefaultRouter()
routers.register('tags', TagViewSet, basename='tags')
routers.register('recipes', RecipeViewSet, basename='recipes')
routers.register('ingredients', IngredientViewSet, basename='ingredients')
routers.register('users', UserViewSet, basename='users')


urlpatterns = [
    path('', include(routers.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
