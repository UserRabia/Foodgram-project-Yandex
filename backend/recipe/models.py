from django.db import models
from colorfield.fields import ColorField
from users.models import User


class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    measurement_unit = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(
        unique=True,
        max_length=200
    )
    color = ColorField(default='#FF0000')

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=200)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe',
        through_fields=('recipe', 'ingredient'),
        related_name='recipes',
    )
    text = models.TextField()
    cooking_time = models.PositiveIntegerField()
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
    )
    image = models.ImageField(
        upload_to='recipe/',
        blank=True,
        null=False,
        default=None
    )

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredientrecipe'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredientrecipe'
    )
    amount = models.PositiveIntegerField()

    def __str__(self):
        return str(self.ingredient)


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='follower'
    )
    author = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='following'
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'author'),
                name='user_author_unique'
            ),
        )


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='followerfavorite'
    )
    favorite = models.ForeignKey(
        Recipe,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='favorite'
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'favorite'),
                name='user_favorite_unique'
            ),
        )


class Cart(models.Model):
    user = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='followercart'
    )
    recipe = models.ForeignKey(
        Recipe,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='recipecart'
    )
