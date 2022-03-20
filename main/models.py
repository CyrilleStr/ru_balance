from django.db import models
import hashlib
import datetime

from array import *


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
        self.hash = hashlib.sha256(
            str(self.amount).encode('utf-8') + str(self.date).encode('utf-8') + str(self.previousId).encode('utf-8') + str(self.creditor).encode('utf-8') + str(self.borrower).encode('utf-8'))


class Relation():
    creditor: User
    borrower: User
    balance: int

    def __init__(self, creditor, borrower, balance):
        self.creditor = creditor
        self.borrower = borrower
        self.balance = balance


class BlockChain(models.Model):

    def createGenesisBlock():
        genesisUser = User()
        genesisUser.name = "Larchuma"
        genesisUser.save()
        block = Block()
        block.createBlock(0, genesisUser, genesisUser)
        block.previousId = 0
        block.calculateHash()
        block.save()

    def addBlock(newBlock: Block):
        newBlock.previousId = Block.objects.latest('date').hash
        newBlock.calculateHash()
        newBlock.save()

    def getAllBlocks():
        currentBlock = Block.objects.latest('date')
        blocks = []
        while currentBlock.previousId != "0":
            blocks.append(currentBlock)
            currentBlock = Block.objects.get(
                hash=currentBlock.previousId)

        return blocks

    def getAllRelation(blocks=0):
        if blocks == 0:
            blocks = BlockChain.getAllBlocks()
        blockExist = False
        relations = []
        for block in blocks:
            blockExist = False
            for relation in relations:
                if (block.creditor == relation.creditor and block.borrower == relation.borrower) or (block.borrower == relation.creditor and block.creditor == relation.borrower):
                    relation.balance += block.amount
                    blockExist = True
            if not blockExist:
                relations.append(
                    Relation(block.creditor, block.borrower, block.amount))

        return relations
