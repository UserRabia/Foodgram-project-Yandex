from django.core.validators import MaxValueValidator
from djoser.serializers import UserSerializer
from drf_extra_fields.fields import Base64ImageField
from recipe.models import (
    Cart,
    Favorite,
    Ingredient,
    IngredientRecipe,
    Recipe,
    Tag,
    User
)
from rest_framework import serializers


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        lookup_field = 'slug'
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        user_id = self.context.get('request').user.id
        return obj.following.filter(id=user_id).exists()


class IngredientRecipeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class IngredientinRecipeCreateSerializer(serializers.ModelSerializer):

    amount = serializers.IntegerField(
        write_only=True,
        validators=[MaxValueValidator(10000)],
        min_value=0
    )
    id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Ingredient
        fields = ('id', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer()
    tags = TagSerializer(many=True)
    ingredients = IngredientRecipeSerializer(
        many=True,
        source='ingredientrecipe'
    )
    is_favorited = serializers.SerializerMethodField(
        read_only=True
    )
    is_in_shopping_cart = serializers.SerializerMethodField(
        read_only=True
    )

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart', 'name',
                  'image', 'text', 'cooking_time')

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        return (request.user.is_authenticated
                and request.user.favorite_user.filter(recipe=obj).exists())

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        return (request.user.is_authenticated
                and request.user.cart_user.filter(recipe=obj).exists())


class RecipeCreateSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    ingredients = IngredientinRecipeCreateSerializer(many=True)
    image = Base64ImageField()
    cooking_time = serializers.IntegerField(
        validators=[MaxValueValidator(1000)],
        min_value=0,
    )

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'ingredients', 'author', 'name',
                  'image', 'text', 'cooking_time')

    def validate(self, validated_data):
        ingredients = validated_data.get('ingredients')
        ingredient_names = [ingredient.get('name')
                            for ingredient in ingredients]
        tags = validated_data.get('tags')
        image = validated_data.get('image')

        if not ingredients or len(ingredient_names) is None:
            raise serializers.ValidationError(
                'Необходимо указать хотя бы один ингредиент.'
            )
        if not tags:
            raise serializers.ValidationError(
                'Необходимо указать хотя бы один тег.'
            )
        if not image and self.context['request'].method == 'POST':
            raise serializers.ValidationError(
                'Необходимо прикрепить изображение.'
            )

        if len(tags) != len(set(tags)):
            raise serializers.ValidationError(
                'Теги должны быть уникальными.'
            )

        if len(ingredient_names) != len(set(ingredient_names)):
            raise serializers.ValidationError(
                'Ингредиенты должны быть уникальными.'
            )

        return validated_data

    def create(self, validated_data):
        tags_data = validated_data.pop('tags')
        ingredients_data = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)

        for tag in tags_data:
            recipe.tags.add(tag)

        for ingredient_data in ingredients_data:
            ingredient_id = ingredient_data.get('id')
            amount = ingredient_data.get('amount')

            if ingredient_id is not None:
                ingredient_obj = Ingredient.objects.get(pk=ingredient_id)
                IngredientRecipe.objects.create(recipe=recipe,
                                                ingredient=ingredient_obj,
                                                amount=amount)
        recipe.save()
        return recipe

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get('cooking_time',
                                                   instance.cooking_time)
        image = validated_data.get('image')
        if image:
            instance.image = image
        tags_data = validated_data.get('tags')
        if tags_data:
            instance.tags.set(tags_data)

        ingredients_data = validated_data.get('ingredients')

        if ingredients_data:
            IngredientRecipe.objects.filter(recipe=instance).delete()
            for ingredient_data in ingredients_data:
                ingredient_id = ingredient_data.get('id')
                amount = ingredient_data.get('amount')
                if ingredient_id is not None:
                    ingredient_obj = Ingredient.objects.get(pk=ingredient_id)
                    IngredientRecipe.objects.create(recipe=instance,
                                                    ingredient=ingredient_obj,
                                                    amount=amount)
        instance.save()
        return instance


class FollowListSerializer(serializers.ModelSerializer):

    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class FollowSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )

    def validate(self, data):
        user = self.context['request'].user
        author = data['author']

        if user == author:
            raise serializers.ValidationError(
                "Вы не можете подписаться на себя!"
            )
        return data

    def get_is_subscribed(self, obj):
        request = self.context['request']
        if request.user.is_authenticated:
            return request.user.follower.filter(author=obj).exists()
        return False

    def get_recipes(self, obj):
        return FollowListSerializer(obj.recipes.all(), many=True).data

    def get_recipes_count(self, obj):
        return obj.recipes.count()


class FavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favorite
        fields = ('user', 'recipe')


class CartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = ('user', 'recipe')
