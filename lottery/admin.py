from django.contrib import admin
from game.models import Option
from .models import (Request, 
                    QuoteManager, 
                    Contest,
                    Ticket,
                    Bet,
                    Prize,
                    Draw)

# Register your models here.
class QuoteManageInLine(admin.TabularInline):
    model = QuoteManager
class RequestInLine(admin.StackedInline):
    model = Request
class BetInLine(admin.TabularInline):
    model = Bet
class PrizeInLine(admin.TabularInline):
    model = Prize
class TicketInLine(admin.TabularInline):
    model = Ticket

class RequestAdmin(admin.ModelAdmin):
    list_display = ('user', 
                    'option', 
                    'quotes',
                    'suggested_numbers', 
                    'price', 
                    'status',)
    readonly_fields = ('price', )

    def save_model(self, request, obj, form, change):
        update_fields = []
        if change:
            if form.cleaned_data['status'] != form.initial['status']:
                update_fields.append('status')
        obj.save(update_fields=update_fields)
        super().save_model(request, obj, form, change)

class TicketAdmin(admin.ModelAdmin):
    list_display = ('option',
                    'status',
                    'quotes_sold')
    readonly_fields = ('quotes_sold',)
    inlines = [QuoteManageInLine,
                BetInLine,]

class BetAdmin(admin.ModelAdmin):
    list_display = ('ticket',
                    'contest',
                    'numbers',
                    'create_date',
                    'status')

class ContestAdmin(admin.ModelAdmin):
    list_display = ('game', 
                    'code', 
                    'status', 
                    'prize',)

class DrawAdmin(admin.ModelAdmin):
    list_display = ('contest',
                    'numbers_drawn',
                    'date')
    inlines = [PrizeInLine, ]

admin.site.register(Ticket,TicketAdmin)
admin.site.register(Request, RequestAdmin)
admin.site.register(Bet, BetAdmin)
admin.site.register(Contest, ContestAdmin)
admin.site.register(Draw, DrawAdmin)