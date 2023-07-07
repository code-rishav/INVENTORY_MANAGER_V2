from django.core.management.base import BaseCommand, CommandError
from stock.models import *
import re

class Command(BaseCommand):

    def handle(self,*args,**kwargs):
        item = Item.objects.all()
        for it in item:
            try:
                stk = Stock.objects.get(item=it)
                if stk.quantity == 0:
                    stk.delete()
                    it.delete()
            except Stock.DoesNotExist:
                it.delete()
                print("Stock not exist")
                
            
            
                
                
                
            
                
        
                
                    
        
            
        
            
    '''def handle(self,*args,**kwargs):
        file = open('D:\INVENTORY_MANAGER_V2-main\stock\pricelist.csv','r',encoding='latin-1')
        content = file.readlines()
        for line in content:
            print("line content",line)
            values = line.split(",")
            name = values[0]
            price = values[1]
            invoiceRate = values[2]
            name = name + " ( "+price+" )"

            pattern = r"(\d+)p"

            match = re.search(pattern,name)

            if match:
                packets = int(match.group(1))
            else:
                packets = 0

            ind = name.index(" ")
            name = name[ind+1:]

            print("Item",name,"\nmrp",price,"\ninvoice",invoiceRate,"\npackets",packets)
            itemobj = Item(name=name,packet=packets,mrp=price,invoice_rate=invoiceRate)
            itemobj.save()
           
            newStock = Stock(item=itemobj,quantity=0)
            newStock.save()
            print("Saved")'''
