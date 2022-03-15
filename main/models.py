from django.db import models
import hashlib
import datetime
import pickle


class User(models.Model):
    name = models.CharField(max_length=255)


class Block(models.Model):
    hash = models.CharField(primary_key=True, max_length=255)
    amount = models.IntegerField()
    creditor = models.ForeignKey(User, on_delete=models.CASCADE)
    borrower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="borrower")
    date = models.DateTimeField()
    previousId = models.CharField(max_length=255)

    def createBlock(self, amount: float, creditor: User, borrower: User):
        self.amount = amount
        self.date = datetime.datetime.now()
        self.creditor = creditor
        self.borrower = borrower
        return self

    def calculateHash(self):
        # picles.dumps() convert object to bytes
        self.hash = hashlib.sha256(
            str(self.amount).encode('utf-8') + str(self.date).encode('utf-8') + str(self.previousId).encode('utf-8') + str(self.creditor).encode('utf-8') + str(self.borrower).encode('utf-8'))


class BlockChain(models.Model):
    genesisBlock = models.ForeignKey(Block, on_delete=models.CASCADE)
    latestBlock = models.ForeignKey(
        Block, on_delete=models.CASCADE, related_name="latestBlock")

    def createGenesisBlock(self):
        genesisUser = User()
        genesisUser.name = "Larchuma"
        genesisUser.save()
        block = Block()
        block.createBlock(0, genesisUser, genesisUser)
        block.previousId = 0
        block.calculateHash()
        block.save()
        self.genesisBlock = Block.objects.get(previousId=0)
        self.latestBlock = Block.objects.get(previousId=0)

    def getlatestBlock(self):
        return latestBlock

    def addBlock(self, newBlock: Block):
        newBlock.previousId = self.latestBlock.hash
        newBlock.calculateHash()
        self.latestBock = newBlock
        newBlock.save()
