from random import random
from decimal import Decimal

from django.db import models


def pick(bias_list):


    print bias_list

    number = "%.18f" % random()
    current = float(0)
    
    process = []
    for x,y in bias_list:
        process.append(y)

    final = weighted(process)
    print process
    print final
    print bias_list[final]
    for choice in bias_list[final]:
        return choice


def weighted(weights):
    total = 0
    winner = 0
    for i, w in enumerate(weights):
        total += w
        if random() * total < w:
            winner = i
    return winner

class BiasedManager(models.Manager):
    """
    Select a *random* banner, from a biased queryset
        - (banners with associated probabilities of being picked)
    """
    def biased_choice(self, **kwargs):
        if 'is_active' in kwargs:
            kwargs.pop('is_active')

        queryset = super(BiasedManager, self).get_query_set()\
            .filter(is_active=True, **kwargs)

        if not queryset.count():
            raise self.model.DoesNotExist

        calculations = queryset.aggregate(weight_sum=models.Sum('weight'))

        bias_list = []
        bias = 0
        for b in queryset:
            bias = b.weight/float(calculations['weight_sum'])
            bias_list.append((b, bias))
        return pick(bias_list)
