from django.db.models import Sum
from django.shortcuts import HttpResponse, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from recipe.models import (
    Cart,
    Favorite,
    Follow,
    Ingredient,
    IngredientRecipe,
    Recipe,
    Tag
)
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from users.models import User
from api.serializers import (
    CartSerializer,
    CustomUserSerializer,
    FavoriteSerializer,
    FollowSerializer,
    IngredientSerializer,
    RecipeCreateSerializer,
    RecipeSerializer,
    TagSerializer
)
from .paginator import CartPaginator, CustomPaginator

from .filters import RecipeFilter
from .permissions import AdminOrAuthorOrReadOnly


class UserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer

    @action(detail=True,
            methods=['post', 'delete'])
    def subscribe(self, request, id):
        user = self.request.user
        author = get_object_or_404(User, id=id)
        follow_exists = Follow.objects.filter(user=user, author=author)
        if request.method == 'POST':
            if user == author:
                return Response(status=status.HTTP_400_BAD_REQUEST)

            if not follow_exists.exists():
                Follow.objects.create(user=user, author=author)
                serializer = FollowSerializer(
                    author, context={'request': request}
                )
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)

        if request.method == 'DELETE':
            if follow_exists.exists():
                follow_exists.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False,
            methods=['get'])
    def subscriptions(self, request):
        follow_list = User.objects.filter(following__user=request.user)
        serializer = FollowSerializer(
            self.paginate_queryset(follow_list),
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    permission_classes = (AdminOrAuthorOrReadOnly,)
    pagination_class = CustomPaginator

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeSerializer
        return RecipeCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def _favorite_or_shopping_cart(self,
                                   request,
                                   pk,
                                   model_name,
                                   serializer_name):
        user = self.request.user
        recipe = get_object_or_404(Recipe, id=pk)
        case_name = model_name.objects.filter(user=user, recipe=recipe)
        if request.method == 'POST':
            if not case_name.exists():
                case_name = model_name.objects.create(user=user, recipe=recipe)
                serializer = serializer_name(
                    case_name, context={'request': request}
                )
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)

        if request.method == 'DELETE':
            if case_name.exists():
                case_name.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post', 'delete'])
    def favorite(self, request, pk):
        return self._favorite_or_shopping_cart(
            request,
            pk,
            Favorite,
            FavoriteSerializer
        )

    @action(
        detail=True,
        methods=['post', 'delete'],
        pagination_class=CartPaginator
    )
    def shopping_cart(self, request, pk):
        return self._favorite_or_shopping_cart(
            request,
            pk,
            Cart,
            CartSerializer
        )

    @action(detail=False, methods=['get'])
    def download_shopping_cart(self, request):
        user = self.request.user
        ingredients_list = (
            IngredientRecipe.objects
            .filter(recipe__cart_recipe__user=user)
            .values('ingredient')
            .annotate(amount_ingredient=Sum('amount'))
            .values_list(
                'ingredient__name',
                'amount_ingredient',
                'ingredient__measurement_unit'
            )
        )

        shopping_list = []
        for ingredient in ingredients_list:
            shopping_list.append('{} - {} {}\n'.format(*ingredient))

        file_shopping_list = HttpResponse(shopping_list,
                                          content_type='text/plain')
        file_shopping_list['Content-Disposition'] = ('attachment; \
                                                     filename={file}.txt')
        Cart.objects.filter(user=user).delete()
        return file_shopping_list
