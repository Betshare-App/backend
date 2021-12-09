from django.contrib import admin
from .models import Game, Option
# Register your models here.

class OptionInline(admin.TabularInline):
    model = Option

class GameAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'is_active')
    inlines = [OptionInline, ]
admin.site.register(Game, GameAdmin)



