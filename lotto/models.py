from django.db import models

class LottoDraw(models.Model):
    round_number = models.PositiveIntegerField(unique=True)
    winning_number1 = models.PositiveSmallIntegerField()
    winning_number2 = models.PositiveSmallIntegerField()
    winning_number3 = models.PositiveSmallIntegerField()
    winning_number4 = models.PositiveSmallIntegerField()
    winning_number5 = models.PositiveSmallIntegerField()
    winning_number6 = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def numbers(self):
        return [
            self.winning_number1,
            self.winning_number2,
            self.winning_number3,
            self.winning_number4,
            self.winning_number5,
            self.winning_number6,
        ]
    
    def __str__(self):
        return f"{self.round_number}회차 당첨번호: {self.numbers()}"
    
class LotteryTicket(models.Model):
    PURCHASE_TYPE_CHOICES = [
        ('manual', '수동'),
        ('auto', '자동'),
    ]

    buyer_name = models.CharField(max_length=50)
    round_number = models.PositiveIntegerField(default=1)
    purchase_type = models.CharField(
        max_length=10,
        choices=PURCHASE_TYPE_CHOICES,
        default='manual',
    )
    number1 = models.PositiveSmallIntegerField()
    number2 = models.PositiveSmallIntegerField()
    number3 = models.PositiveSmallIntegerField()
    number4 = models.PositiveSmallIntegerField()
    number5 = models.PositiveSmallIntegerField()
    number6 = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def numbers(self):
        return [
            self.number1,
            self.number2,
            self.number3,
            self.number4,
            self.number5,
            self.number6,
        ]
    
    def match_count(self, draw):
        return len(set(self.numbers()) & set(draw.numbers()))
    
    def __str__(self):
        return f"{self.buyer_name}님의 {self.round_number}회차 로또 티켓: {self.numbers()} ({self.purchase_type})  "
    
    