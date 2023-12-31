from django.contrib import admin

from recipe.models import Tag, Recipe, Ingredient, IngredientRecipe, Follow


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    pass


class IngredientRecipeInLine(admin.StackedInline):
    model = IngredientRecipe
    extra = 1


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [IngredientRecipeInLine]


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    pass
