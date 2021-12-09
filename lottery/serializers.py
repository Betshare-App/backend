from django.db.models import fields
from rest_framework import serializers, validators
from lottery.models import (QuoteManager, 
                            Bet, 
                            Request,
                            Contest,
                            Ticket)
from game.models import (Game, Option)

class ContestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contest
        fields = '__all__'

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ('id', 'numbers', 'price', 'chance','quote_value')

class GameSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True)
    class Meta:
        model = Game
        fields = ('name', 'color', 'is_active', 'options', 'total_numbers', 'total_queues')

class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ('id', 'user', 'option', 'quotes', 'price', 'status')
    
class sendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ('user', 'option', 'quotes', 'suggested_numbers')

class BetSerializer(serializers.ModelSerializer):
    contest = ContestSerializer()
    class Meta:
        model = Bet
        fields = ('ticket', 'contest', 'numbers', 'status')

class GameName(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('name',)

class OptionTickets(serializers.ModelSerializer):
    game = GameName()
    class Meta:
        model = Option
        fields = ('game', 'numbers', 'price', 'chance', 'quote_value')

class TicketSerializer(serializers.ModelSerializer):
    option = OptionTickets()
    class Meta:
        model = Ticket
        fields = ('id', 'option', 'status', 'quotes_sold')

class QuoteValue(serializers.ModelSerializer):
    game = GameName()
    class Meta:
        model = Option
        fields = ('game','quote_value','numbers')

class CartSerializer(serializers.ModelSerializer):
    option = QuoteValue()
    class Meta:
        model = Request
        fields = ('id', 'option', 'quotes', 'price')

class QuoteManagerSerializer(serializers.ModelSerializer):
    ticket = TicketSerializer()
    request = RequestSerializer()
    class Meta:
        model = QuoteManager
        fields = ('ticket','request','transaction','quotes')