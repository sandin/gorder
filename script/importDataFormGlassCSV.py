# -*- coding: utf-8 -*-
'''
Created on 2011-12-2

@author: lds
'''
from datetime import datetime
from gorder.order.models import Order, GlassRow
from gorder.script.formatGlassCVS import fixGlassCSV
import string
import sys

CLIENT = "家和-"

def main():
    filename = sys.argv[1]
    fixGlassCSV(filename)
    
    fileIn = open(filename, 'r')
    lines = fileIn.readlines()
    lastLine = ""
    lastOrder = createOrder(CLIENT+"0")
    for i in len(lines):
        l = lines[i]
        if not l or "\r\n" == l:
            if not lastLine: # two block line a raw
                continue
            # block line mean a new order
            order = createOrder(CLIENT+string(i+1))
            print "create a new order: " + order
            #order.save()
            lastOrder = order
        else:
            l = l.replace("\r\n", "")
            data = l.split(",")
            if (len(data) != 6):
                raise Exception("data format wrong :" + data)
            mode = int(data[0])
            glassType = data[1]
            width = float(data[2])
            height = float(data[3])
            quantity = int(data[4])
            rub = data[5]
            unitPrice = findPriceByGlassType(glassType) if (mode!=0) else 0
            row = GlassRow.create(name='row', quantity=quantity,
                                  unitPrice=unitPrice, orderId=lastOrder,
                                  width=width, height=height,
                                  rate=1.2, rubEdge=rub, rubEdgeUnitPrice=0.8,
                                  extra="", extraCost=0)
            print "create a row :" + row
            #row.save()
            lastLine = l
            
PRICE = {"5":25, "51":40, "52":52, "8":40, "9":50}
            
def findPriceByGlassType(glassType):         
    if (PRICE.has_key(glassType)):
        return PRICE[glassType]
    else:
        return 0;
    
def createOrder(clientName):
    return Order(client=clientName, phone=0, date=datetime.now(), price=0, cash=0, status=0, note="");
        
    
main()
