from django.contrib import admin


from .models import *


admin.site.register(Spice)
admin.site.register(PlaceSpice)
admin.site.register(Ingredient)
admin.site.register(IngredientItem)
admin.site.register(PlaceIngredient)
admin.site.register(CookStage)
admin.site.register(Food)