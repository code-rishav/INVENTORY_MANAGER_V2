from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.html import format_html
import json
from json import dumps
from django.core import serializers

from stock.models import * 
from django.http import HttpResponseRedirect,JsonResponse
from django.template.loader import render_to_string
from django.template.loader import get_template
# Create your views here.
def dealer(request,slug=None):
    dealer = get_object_or_404(Dealer,slug=slug)

    return render(request,'stock/dealer.html',{'dealer':dealer})


def index(request):
    items = Item.objects.all()
    purchase = reversed(Purchase.objects.all())
    sale = reversed(Sale.objects.all())
    stock = Stock.objects.all()
    dealers = Dealer.objects.all()
    recievings = Recieving.objects.all()
    context = {'items':items,'purchase':purchase,'sale':sale,'stock':stock,'dealers':dealers,'recievings':recievings}
    return render(request,'stock/stocks.html',context)

def detail(request,id=None):
    purchase = get_object_or_404(Purchase,id=id)
    return render(request,'stock/detail.html',{'purchase':purchase})





def entryForm(request):

    all_items = Item.objects.all()
    if request.method=="POST":
        if request.POST.get("newItem"):
            item = request.POST.dict()
            name = item.get("itemname")
            packets = item.get("packets")
            mrp = item.get("mrp")
            invoiceRate = item.get("invoice-rate")

            newItem = Item(name=name,packet=packets,mrp=mrp,invoice_rate=invoiceRate)
            newItem.save()

            #add this item to stock table
            sitem = Item(name=name)
            newStock = Stock(item=sitem,quantity=0)
            newStock.save()

        elif request.POST.get("newPurchase"):
            purchase = request.POST.dict()
            itemobj = Item(name=purchase.get("item"))
            item  = Item.objects.get(name=itemobj.name)
            quantity = purchase.get("quantity")
            date = purchase.get("date")
            amount = float(quantity) * float(item.invoice_rate)
            print("post method items",quantity,date,item,amount,"Item invoice rate",item.invoice_rate)

            newPurchase = Purchase(item=item,quantity=quantity,date=date,amount=amount)
            newPurchase.save()

            #update the stock table
            items = Stock.objects.get(item=item)
            items.quantity = items.quantity + int(quantity)
            items.save()
    
    return render(request,'stock/sale-form.html',{'items':all_items})


def generateBill(request):
    print("in generate bills***************")
    items = Item.objects.all()
    billItem = dict()
    countItem = 0
    #retrieve all necessary data to send to the html page
    buyer = Dealer.objects.all()
    buyer_json = serializers.serialize('json',  buyer)


    if request.method=="POST":
        print("after post method")
        print("inside submit call")
        data = json.loads(request.body)

        #generate invoice data and add it to database
        dealername = data.get('dealer')
        totalSum = data.get('finalSum')
        invoiceId = data.get('invoiceId')
        invoiceDate = data.get('invoiceDate')
        print(dealername,totalSum,invoiceId,invoiceDate)
        
        #update dealer data
        dealer = Dealer.objects.get(name=dealername)
        dealer.balance = float(dealer.balance) + float(totalSum)
        dealer.save()
        


        invoice = Invoice(invoiceId=invoiceId,date=invoiceDate,dealer=dealer,amount=totalSum)
        invoice.save()

        #create data for sales table
        
        
        table_data =  data.get('tabledata',[])
        print("data in post method")
        print(table_data)

        for row in table_data:
            updateTables(row,dealer)
        

        return render(request,'stock/bill-template.html',{'items':items,'dealer':dealer})
        

    return render(request,'stock/bill-template.html',{'buyer':buyer,'items':items,'buyer_json':buyer_json})
    


def updateTables(row,dealer):
    name = row['item']
    rate = float(row['rate'])
    quantity = int(row['quantity'])
    total = float(row['total'])

    item = Item(name=name)
    itemS = Stock.objects.get(item=item)
    itemS.quantity = itemS.quantity - int(quantity)
    itemS.save()

    #create sale entry
    sale = Sale(item=item,quantity=quantity,rate=rate,dealer=dealer,amount=total)
    print(sale)
    sale.save()
    return


def createBill(request):
    item = Item.objects.all()

    return render(request,'stock/bill-template.html',{'items':item})



def updateAccounts(request):

    dealers = Dealer.objects.all()
    if request.method == "POST":
        data = request.POST.dict()
        name = data.get("dealer")
        date = data.get("date")
        amount = float(data.get("amount"))

        print(name,date,amount)

        dealer = Dealer(name=name)

        #update the balance amount 
        updateDealer = Dealer.objects.get(name=dealer.name)
        updateDealer.balance = float(updateDealer.balance) - (amount)
        updateDealer.save()
        
        

        recieving = Recieving(dealer=dealer,date=date,amount=amount)
        recieving.save()


    return render(request,'stock/accounts-update.html',{'dealers':dealers})