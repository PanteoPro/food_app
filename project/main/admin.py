from django.contrib import admin

from .models import Profile, EatCook, EatIngredient

admin.site.register(Profile)
admin.site.register(EatCook)
admin.site.register(EatIngredient)
