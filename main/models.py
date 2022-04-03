from django.db import models
import hashlib
import datetime

from array import *


class User(models.Model):
    name = models.CharField(max_length=255)


class Relation(models.Model):
    creditor = models.ForeignKey(User, on_delete=models.CASCADE)
    borrower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="borrower")
    balance = models.FloatField()

    def udpateBalance(self, amount):
        self.balance += amount
        if self.balance < 0:
            self.borrower, self.creditor = self.creditor, self.borrower
            self.balance *= -1
