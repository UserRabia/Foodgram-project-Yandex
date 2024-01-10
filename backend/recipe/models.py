from colorfield.fields import ColorField
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.db import models
from foodgram.constants import FIXED_STRING_LENGTH
from users.models import User


class Ingredient(models.Model):
    name = models.CharField(
        max_length=FIXED_STRING_LENGTH,
        verbose_name='Название'
    )
    measurement_unit = models.CharField(
        max_length=FIXED_STRING_LENGTH,
        verbose_name='Единица меры'
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(
        max_length=FIXED_STRING_LENGTH,
        verbose_name='Название'
    )
    slug = models.SlugField(
        unique=True,
        max_length=FIXED_STRING_LENGTH,
        verbose_name='Слаг'
    )
    color = ColorField(
        default='#FF0000',
        verbose_name='Цвет'
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(
        max_length=FIXED_STRING_LENGTH,
        verbose_name='Название'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe',
        through_fields=('recipe', 'ingredient'),
        related_name='recipes',
        verbose_name='Ингредиенты'
    )
    text = models.TextField(verbose_name='Описание')
    cooking_time = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(1000)],
        verbose_name='Время приготовления'
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Теги'
    )
    image = models.ImageField(
        upload_to='recipe/',
        blank=True,
        null=False,
        default=None,
        verbose_name='Изображение'
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-id']

    def __str__(self):
        return self.name


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredientrecipe',
        verbose_name='Ингредиент'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredientrecipe',
        verbose_name='Рецепт'
    )
    amount = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(10000)],
        verbose_name='Количество'
    )

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингрединты в рецептах'

    def __str__(self):
        return str(self.ingredient)


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Пользователь'
    )
    author = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'author'),
                name='user_author_unique'
            ),
        )

    def validate(self):
        if self.user == self.author:
            raise ValidationError(
                'Вы не можете подписаться на самого себя'
            )


class FavoriteOrCartBaseModel(models.Model):
    user = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='%(class)s_user',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='%(class)s_recipe',
        verbose_name='Рецепт'
    )

    class Meta:
        abstract = True
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='%(class)s_unique'
            ),
        )


class Favorite(FavoriteOrCartBaseModel):

    class Meta(FavoriteOrCartBaseModel.Meta):
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'


class Cart(FavoriteOrCartBaseModel):

    class Meta(FavoriteOrCartBaseModel.Meta):
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'
