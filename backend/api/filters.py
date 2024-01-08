from django_filters.rest_framework import (FilterSet,
                                           filters,
                                           ModelMultipleChoiceFilter)
from recipe.models import Favorite, Cart, Tag, Recipe, User


class RecipeFilter(FilterSet):
    author = filters.ModelChoiceFilter(queryset=User.objects.all())
    is_favorited = filters.BooleanFilter(
        method='filter_is_favorited'
    )
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_is_in_shopping_cart'
    )
    tags = ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )

    def filter_is_favorited(self, queryset, name, value):
        user = self.request.user
        if value:
            favorites = Favorite.objects.filter(user=user).values_list(
                'recipe'
            )
            return queryset.filter(id__in=favorites)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if value:
            cart_items = Cart.objects.filter(user=user).values_list('recipe')
            return queryset.filter(id__in=cart_items)
        return queryset

    class Meta:
        model = Recipe
        fields = (
            'tags',
            'is_favorited',
            'is_in_shopping_cart',
            'author'
        )
