from django.db import models

class Record(models.Model):
    BIG = 'BIG'
    SMALL = 'SMALL'
    DNP = 'did not predict'
    WIN = 'WIN'
    LOSS = 'LOSS'

    COLOR_0 = "RED/VIOLET"
    COLOR_5 = "GREEN/VIOLET"
    COLOR_EVEN = "RED"
    COLOR_ODD = "GREEN"

    COLOUR_CHOICES = [
        (COLOR_0, COLOR_0),
        (COLOR_5, COLOR_5),
        (COLOR_EVEN, COLOR_EVEN),
        (COLOR_ODD, COLOR_ODD),
    ]

    SIZE_CHOICES = [
        (BIG, BIG),
        (SMALL, SMALL),
        (DNP, DNP),
    ]

    issue_number = models.BigIntegerField(unique=True, primary_key = True)
    premium = models.IntegerField()
    level = models.IntegerField(default = 0)
    is_win = models.BooleanField(default = False)

    number = models.IntegerField(default=0)
    colour = models.CharField(max_length=255, choices=COLOUR_CHOICES,default="not available")
    size = models.CharField(max_length=20, choices=SIZE_CHOICES, default=BIG)

    predicted_number = models.IntegerField(default=0)
    predicted_colour = models.CharField(max_length=255, choices=COLOUR_CHOICES, default="not available")
    predicted_size = models.CharField(max_length=20, choices=SIZE_CHOICES, default=DNP)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.issue_number} - {self.number} - {self.colour} - {self.premium}"
