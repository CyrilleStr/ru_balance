from django.db import models
import hashlib
import datetime

class User(models.Model):
    name = models.CharField(max_length=255)

class Block(models.Model):
    hash = models.CharField(primary_key=True,max_length=255)
    amount  = models.IntegerField()
    creditor = models.ForeignKey(User, on_delete=models.CASCADE)
    borrower = models.ForeignKey(User, on_delete=models.CASCADE,related_name="borrower")
    date = models.DateTimeField()
    previousId = models.CharField(max_length=255)

    # def __init__(self):
        # self.amount = amount
        # self.date = date
        # self.previousId = previousId

    def calculateHash():
        self.hash = hashlib.sha256(amount + date + previousID + str(creditor) + str(borrower))

class BlockChain(models.Model):
    genesisBlock = models.ForeignKey(Block, on_delete=models.CASCADE)
    latestBlock = models.ForeignKey(Block, on_delete=models.CASCADE,related_name="latestBlock")

    def createGenesisBlock():
        self.chain = Block()
        block.amount = 0
        block.date = datetime.datetime.now()
        block.previousId = 0
        block.creditor = None
        block.borrower = None
        block.calculatedHash()


    def getlatestBlock():
        return latestBlock

    def addBlock(newBlock):
        newBlock.previousId = self.getLatestBlock().hash;
        newBlock.calculateHash();
        self.latestBock = newBlock