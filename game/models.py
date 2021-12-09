from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ForeignKey
from lottery.config.constants import MAX_QUOTES, TAX
# Create your models here.
class Game(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    total_numbers = models.IntegerField()
    total_queues = models.IntegerField()
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class Option(models.Model):
    game = ForeignKey(Game, on_delete=CASCADE, related_name='options')
    numbers = models.IntegerField()
    price = models.FloatField()
    chance = models.FloatField(blank=True, null=True)
    quote_value = models.FloatField()

    def __str__(self):
        return self.game.name + "(" + str(self.numbers) + ")"

    def save(self, *args):
        self.quote_value = round((self.price / MAX_QUOTES)*(1 + TAX), 2)
        super(Option, self).save(*args)
    
