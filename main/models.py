from django.db import models
import hashlib
import datetime

from array import *


class User(models.Model):
    name = models.CharField(max_length=255)


class Block(models.Model):
    id = models.IntegerField(primary_key=True)
    hash = models.CharField(max_length=255)
    amount = models.IntegerField()
    creditor = models.ForeignKey(User, on_delete=models.CASCADE)
    borrower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="borrower")
    date = models.DateTimeField()
    previousHash = models.CharField(max_length=255)

    def createBlock(self, amount: float, creditor: User, borrower: User):
        self.amount = amount
        self.date = datetime.datetime.now()
        self.creditor = creditor
        self.borrower = borrower
        return self

    def calculateHash(self):
        self.hash = hashlib.sha256(
            str(self.amount).encode('utf-8') + str(self.date).encode('utf-8') + str(self.previousHash).encode('utf-8') + str(self.creditor).encode('utf-8') + str(self.borrower).encode('utf-8'))


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
        genesisUser: User
        try:
            genesisUser = User.objects.get(name="Larchuma")
        except(KeyError, User.DoesNotExist):
            genesisUser = User()
            genesisUser.name = "Larchuma"
            genesisUser.save()
        block = Block()
        block.createBlock(0, genesisUser, genesisUser)
        block.previousHash = 0
        block.calculateHash()
        block.save()

    def addBlock(newBlock: Block):
        newBlock.previousHash = Block.objects.order_by('id').last().hash
        newBlock.calculateHash()
        newBlock.save()

    def getAllBlocks():
        blocks = []
        currentBlock = Block.objects.order_by('id').last()
        if currentBlock != None:
            while currentBlock.previousHash != "0":
                blocks.append(currentBlock)
                currentBlock = Block.objects.get(
                    hash=currentBlock.previousHash)
        return blocks

    def getAllRelation(blocks=0):
        if blocks == 0:
            blocks = BlockChain.getAllBlocks()
        relations = []
        blockExist = False
        for block in blocks:
            blockExist = False
            for relation in relations:
                if (block.creditor == relation.creditor and block.borrower == relation.borrower) or (block.borrower == relation.creditor and block.creditor == relation.borrower):
                    relation.balance += block.amount
                    blockExist = True
                if relation.balance < 0:
                    relation.borrower, relation.creditor = relation.creditor, relation.borrower
                    relation.balance *= -1
            if not blockExist:
                relations.append(
                    Relation(block.creditor, block.borrower, block.amount))

        return relations

    def relationExist(creditor, borrower):
        relations = BlockChain.getAllRelation()
        for relation in relations:
            if ((creditor == relation.creditor) and (borrower == relation.borrower)) or ((creditor == relation.borrower) and (borrower == relation.creditor)):
                return True
        return False
