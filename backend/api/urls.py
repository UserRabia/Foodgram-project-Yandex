from django.urls import include, path
from rest_framework import routers

from api.views import (
    IngredientViewSet,
    RecipeViewSet,
    TagViewSet,
    UserViewSet
)

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
