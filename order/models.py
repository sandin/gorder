# -*- coding: utf-8 -*-
from django.db import models
import datetime

# Create your models here.
class Order(models.Model):
    client = models.CharField(max_length=200)
    phone = models.CharField(max_length=13)
    date = models.DateTimeField()
    price = models.FloatField()
    cash = models.FloatField() #TODO 
    status = models.IntegerField()
    note = models.TextField(blank=True, null=True)
    
    @staticmethod
    def create(clientName):
        return Order(client=clientName, phone=0, date=datetime.datetime.now(), price=0, cash=0, status=0, note="");

    def __unicode__(self):
        return self.client

class Product(models.Model):
    name = models.CharField(max_length=200)
    incomingPrice = models.FloatField()
    outgoingPrice = models.FloatField()

class GlassRow(models.Model):
    name = models.CharField(max_length=200) # 名称
    quantity = models.IntegerField() # 数量
    unitPrice = models.FloatField()  # 单价
    price = models.FloatField()  # 金额
    orderId = models.ForeignKey(Order)
    width = models.IntegerField() # 尺寸  
    height = models.IntegerField() # 尺寸
    rate = models.FloatField() # 损耗率,一般为1.2
    rubEdge = models.CharField(max_length=2) # 00 or 22
    rubEdgeCost = models.FloatField() ## 磨边金额
    rubEdgeUnitPrice = models.FloatField() # 磨边单价
    extra = models.CharField(max_length=100,blank=True, null=True) # 额外费用名称
    extraCost = models.FloatField(blank=True, null=True) # 额外费用
    glassPrice = models.FloatField() ## 仅玻璃金额

    @staticmethod
    def create(*args, **kargs):
        width = float(kargs['width'])
        height = float(kargs['height'])
        rubEdge = kargs['rubEdge']
        rate = float(kargs['rate'])
        unitPrice = float(kargs['unitPrice'])
        rubEdgeUnitPrice = float(kargs['rubEdgeUnitPrice'])
        extraCost = float(kargs['extraCost'])
        quantity = int(kargs['quantity'])

        rubEdgeCost = GlassRow.calRubEdgeCost(width, height, quantity, int(rubEdge[0]), int(rubEdge[1]), rubEdgeUnitPrice)
        glassPrice = GlassRow.calGlassPrice(width, height, quantity, rate, unitPrice)
        price = glassPrice + rubEdgeCost + extraCost
        kargs['rubEdgeCost'] = rubEdgeCost
        kargs['glassPrice'] = glassPrice
        kargs['price'] = price
        return GlassRow(*args, **kargs)

    @staticmethod
    def calRubEdgeCost(width, height, quantity, widthRub, heightRub, unitPrice):
        return unitPrice * quantity * (width * widthRub + height * heightRub)/1000

    @staticmethod
    def calGlassPrice(width, height, quantity, rate, unitPrice):
        return width*height*quantity*rate*unitPrice/1000000

    def __unicode__(self):
        return str(self.width) + "x" + str(self.height)

    def __str__(self):
        return str(self.width) + "x" + str(self.height)