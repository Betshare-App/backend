from django.db import models
from django.db.models.deletion import CASCADE, DO_NOTHING, SET_NULL
from django.db.models.fields.related import ForeignKey, ManyToManyField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.http import request
from rest_framework import status
from game.models import Option, Game
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from .config.constants import MAX_QUOTES
# Create your models here.

class RequestStatus(models.Choices):
    OPEN = "open"
    PAID = "paid"
    CANCELED = "canceled"
    FINISHED = 'finished'

class Request(models.Model):
    user = models.ForeignKey(User, on_delete=SET_NULL, related_name='userrequest', null=True)
    option = models.ForeignKey(Option, on_delete=DO_NOTHING, related_name='option')
    quotes = models.IntegerField()
    price =  models.FloatField(null=True, blank=True)
    suggested_numbers = models.CharField(max_length=250)
    status = models.CharField(max_length=50, choices=RequestStatus.choices, default=RequestStatus.OPEN)

    def __str__(self):
        return self.user.username + "(" + str(self.quotes) + ")"

    def save(self, *args, **kwargs):
        self.price = round((self.option.quote_value * self.quotes),2) 
        super(Request, self).save(*args, **kwargs)

class ContestStatus(models.Choices):
    PENDING = 'pending' 
    FINISHED = 'finished'

class Contest(models.Model):
    code = models.IntegerField()
    game = models.ForeignKey(Game, on_delete=DO_NOTHING)
    status = models.CharField(max_length=50, choices=ContestStatus.choices, default=ContestStatus.PENDING)
    prize = models.FloatField(default=1)

    def __str__(self):
        return self.game.name + " " + str(self.code)

class TicketStatus(models.Choices):
    OPEN = 'open'
    CLOSED = 'closed'
    FINISHED = 'finished'

class Ticket(models.Model):
    option = ForeignKey(Option, on_delete=CASCADE, related_name='ticketoption')
    status = models.CharField(max_length=50, default=TicketStatus.OPEN)
    requests = models.ManyToManyField(Request, through='QuoteManager', null=True, default=None, related_name='ticketrequests')
    quotes_sold = models.IntegerField(
        validators=[
            MaxValueValidator(MAX_QUOTES),
            MinValueValidator(0)
        ], default=0)
    
    def __str__(self):
        return self.option.game.name + "(" + str(self.id) + ")"
    
    def save(self, *args):
        try:
            if(self.requests != None):
                quotes_sold = 0
                quote_managers = QuoteManager.objects.filter(ticket=self)
                for req in quote_managers:
                    quotes_sold += req.quotes
                self.quotes_sold = quotes_sold
            if(self.quotes_sold == 250):
                if(self.status != TicketStatus.CLOSED):
                    self.status = TicketStatus.CLOSED
            elif(self.quotes_sold > 250):
                raise Exception("Cotas vendidas superaram as cotas máximas")
        except:
            pass
        super(Ticket, self).save(*args)

class QuoteManager(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=CASCADE, null=True,blank=True)
    request = models.ForeignKey(Request, on_delete=CASCADE, related_name='quote_manager', null=True, blank=True)
    transaction = models.CharField(max_length=250, null=True, blank=True)
    quotes = models.IntegerField(default=0) 

class BetStatus(models.Choices):
    PENDING = 'pending'
    NO_PRIZE = 'no_prize'
    WITH_PRIZE = 'with_prize'

class Bet(models.Model):
    ticket = models.OneToOneField(Ticket, on_delete=CASCADE)
    contest = ForeignKey(Contest, on_delete=CASCADE)
    numbers = models.CharField(max_length=250)
    create_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=BetStatus.choices, default=BetStatus.PENDING)

class Draw(models.Model):
    contest = models.OneToOneField(Contest, on_delete=DO_NOTHING)
    numbers_drawn = models.CharField(max_length=250, null=True, blank=True)
    date = models.DateField()

class Prize(models.Model):
    draw = models.ForeignKey(Draw, on_delete=CASCADE)
    numbers = models.PositiveIntegerField()
    value = models.FloatField()
    winners = models.IntegerField()

class UserPrize(models.Model):
    user = models.ForeignKey(User, on_delete=SET_NULL, null=True)
    request = models.ForeignKey(Request, on_delete=CASCADE)
    value = models.FloatField()
    proof = models.ImageField()

def post_save_config(sender, **kwargs):
    instance = kwargs['instance']
    quote_manager=None
    if(instance.status == str(RequestStatus.PAID)):
        qm = QuoteManager.objects.filter(request=instance)
        if(len(qm) == 0):
            quote_manager = create_quote_manager(instance)
    return quote_manager

def get_ticket(request):
    ticket = None
    try:
        ticket = Ticket.objects.filter(
            status=str(TicketStatus.OPEN),
            quotes_sold__lt=250).get(
            option=request.option.id)
    except Ticket.DoesNotExist:
        ticket = Ticket(option=request.option)
        ticket.save()
    return ticket

def create_quote_manager(request, quotes=0):
    ticket = get_ticket(request)
    quotes_sold, quotes_rest = 0, 0
    quote_manager = None
    manage_quotes = quotes if quotes else request.quotes
    try:
        qm = QuoteManager.objects.filter(
            ticket=ticket)
        
        for q in qm:
            quotes_sold += q.quotes
        quotes_rest = MAX_QUOTES - quotes_sold
        
        if(quotes_rest >= manage_quotes):
            quote_manager = QuoteManager(
                quotes = manage_quotes,
                ticket = ticket,
                request = request)
        else:
            quote_manager = QuoteManager(
                quotes = quotes_rest,
                ticket = ticket,
                request = request)
            ticket.status = TicketStatus.CLOSED
            ticket.save()
            new_quotes = manage_quotes - quotes_rest
            create_quote_manager(request, new_quotes)

    except QuoteManager.DoesNotExist:
        quotes_rest = MAX_QUOTES
        quote_manager = QuoteManager(
            quotes = manage_quotes,
            ticket = ticket,
            request = request
        )
    quote_manager.save()
    ticket.save()
    return quote_manager

post_save.connect(post_save_config, sender=Request)