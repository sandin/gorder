# coding:utf-8
from django.http import HttpResponse
from django.shortcuts import render_to_response
from gorder.order.models import GlassRow, Order
import datetime
import logging

logging.basicConfig(filename='example.log',level=logging.DEBUG)
logger = logging.getLogger(__name__)

def create(request):
    if request.method == 'GET':
        return render_to_response('order/create.html', {})
    elif request.method == "POST":
        data = []
        for i in range(1,1000):
            if not request.POST.has_key('glass-width-'+str(i)):
                break # end of loop
            width = request.POST['glass-width-'+str(i)]
            if not width:
                continue
            name = request.POST['glass-name-'+str(i)]
            height = request.POST['glass-height-'+str(i)]
            quantity = request.POST['glass-quantity-'+str(i)]
            rate = request.POST['glass-rate-'+str(i)]
            unitPrice = request.POST['glass-unitPrice-'+str(i)]
            rubEdge = request.POST['glass-rubEdge-'+str(i)]
            extra = request.POST['glass-extra-'+str(i)]
            extraCost = request.POST['glass-extraCost-'+str(i)]
            if width and height and quantity and rate and unitPrice and rubEdge:
                width = float(width)
                height = float(height)
                quantity = int(quantity)
                rate = float(rate) if rate > 1.0 else 1.2
                unitPrice = float(unitPrice)
            extraCost = float(extraCost) if extraCost else 0
            data.append([name, width, height, quantity, rate, unitPrice, rubEdge, extra, extraCost])
        data = fixData(data)
        client

        return render_to_response('order/createResult.html', locals())

def fixData(dataList):
    data = []
    lastRow = ['unknown',0,0,0,0,0,'00',"",0]
    for d in dataList:
        if not d[0]: # name
            d[0] = lastRow[0]
        if len(d[6]) == 0: # rubEdge
            d[6] = '00'
        data.append(d)
        lastRow = d
    return data

def importDataFormCSV(request):
    if request.method == 'GET':
        return render_to_response('script/importCSV.html', {})
    elif request.method == "POST":
        if request.POST.has_key('data'):
            data = importData(request.POST['data'])
            return render_to_response('script/importCSV.html', {'data':data})
        else:
            return render_to_response('script/importCSV.html', {'error':"miss data"})

    filename = request.GET['filename']
    importData(filename)

def listOrder(request):
    subtitle = "Orders details"
    if request.GET.has_key('month'):
        month = int(request.GET['month'])
        orders = Order.objects.filter(date__month=month)
        subtitle += " - Month " + str(month)
    else:
        orders = Order.objects.all()[:200]
    total_price = 0
    for o in orders:
        for row in o.glassrow_set.all():
            total_price += float(row.price)
    return render_to_response('order/listOrder.html', {'orders':orders, 'total_price': total_price, 'subtitle': subtitle})

def fixGlassCSV(data):
    newStr = "";
    line = data.split("\n")
    lastLine = []
    for l in line:
        if l.startswith('#'):
            continue
        if not l or l == '\n': 
            newStr += '\n'
            continue
    
        #l = l.replace(r"\n", "")
        l = l.strip()
        data = l.split(',')
        if (len(data) == 3):
            data = [lastLine[0], lastLine[1], data[0], data[1], data[2], lastLine[5]]
        elif (len(data) == 4):
            data = [lastLine[0], lastLine[1], data[0], data[1], data[2], data[3]]

        newStr += ','.join(data) + '\n'
        lastLine = data
    
    return newStr

def importData(dataStr):
    CLIENT = "家和-"
    data = fixGlassCSV(dataStr)
    data = data.strip() 
    lines = data.split("\n")
    lastLine = ""
    lastOrder = Order.create(CLIENT+"0")
    lastOrder.save()
    for i in range(len(lines)):
        l = lines[i]
        logger.info(i)
        if not l or "\n" == l:
            if not lastLine: # two block line a raw
                continue
            # block line mean a new order
            order = Order.create(CLIENT+str(i+1))
            logger.info("create a new order")
            order.save()
            lastOrder = order
        else:
            #l = l.replace("\r\n", "")
            l = l.strip()
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
            glassName = getGlassNameByGlassType(glassType)
            row = GlassRow.create(name=glassName, quantity=quantity,
                                  unitPrice=unitPrice, orderId=lastOrder,
                                  width=width, height=height,
                                  rate=1.2, rubEdge=rub, rubEdgeUnitPrice=0.8,
                                  extra="", extraCost=0)
            logger.info("create a row " + str(row))
            row.save()
            lastLine = l
    return lines

GLASSTYPE = {
    "5":  {'name': '5mm', 'price': 25},
    "51": {'name': '5mm银镜', 'price': 40},
    "52": {'name': '5mm黑镜', 'price': 44},
    "8":  {'name': '8mm', 'price': 40},
    "9":  {'name': '9mm', 'price': 50},
}
            
def findPriceByGlassType(glassType):         
    if (GLASSTYPE.has_key(glassType)):
        return GLASSTYPE[glassType]['price']
    else:
        return 0;

def getGlassNameByGlassType(glassType):         
    if (GLASSTYPE.has_key(glassType)):
        return GLASSTYPE[glassType]['name']
    else:
        return "-";
