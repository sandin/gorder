"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from datetime import datetime
from django.test import TestCase
from order.models import GlassRow, Order

class SimpleTest(TestCase):

    def testGlassRow(self):
        order = Order(client="test-order", phone=0, date=datetime.now(), price=0, cash=0, status=0, note="");
        order.save()
        orderInDb = Order.objects.get(id=order.id)
        self.assertEquals(order.id, orderInDb.id)
        print Order.objects.all()

        # test insert row
        row = GlassRow.create(name='testrow', quantity=2, unitPrice=45, orderId=order, width=162, height=517, rate=1.2, rubEdge='22', rubEdgeUnitPrice=1, extra="", extraCost=0)
        row.save()
        rowInDb = GlassRow.objects.get(id=row.id)
        self.assertEquals(row.id, rowInDb.id)
        print GlassRow.objects.all()

        # test cal
        width = 382
        height = 1490
        quantity = 2
        unitPrice = 50
        expectPrice = 74.292
        row2 = GlassRow.create(name="testrow", quantity=quantity, unitPrice=unitPrice, orderId=order, width=width, height=height, rate=1.2, rubEdge="22", rubEdgeUnitPrice=0.8, extra="", extraCost=0)
        self.assertEquals(68.3016, row2.glassPrice)
        self.assertEquals(5.9904, row2.rubEdgeCost)
        self.assertTrue(expectPrice - row2.price < 0.01) # 




