from django.db import models

class Record(models.Model):
    BIG = 'big'
    SMALL = 'small'
    DNP = 'did not predict'
    WIN = 'win'
    LOSS = 'loss'

    PREDICTION_CHOICES = [
        (BIG, BIG),
        (SMALL, SMALL),
        (DNP, DNP),
    ]
    SIZE_CHOICES = [
        (BIG, BIG),
        (SMALL, SMALL)
    ]

    issue_number = models.BigIntegerField(unique=True, primary_key = True)
    number = models.IntegerField()
    colour = models.CharField(max_length=255)
    premium = models.IntegerField()
    size_prediction = models.CharField(max_length=20, choices=PREDICTION_CHOICES, default=DNP)
    size = models.CharField(max_length=20, choices=SIZE_CHOICES, default=BIG)
    level = models.IntegerField(default = 0)
    is_win = models.BooleanField(default = False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.issue_number} - {self.number} - {self.colour} - {self.premium}"
