from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import OrderSerializer, WalletSerializer
from agents.models import Wallet, Agent, Order
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from products.models import Products
from account.models import Account
from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail, EmailMultiAlternatives
from azabazar import settings
from django.http import Http404
from rest_framework import status

@api_view(['POST'], )
def orderAPI(request):
    if request.method == 'POST':
        data = request.data
        total = data['total']
        total = float(total)
        wallet = data["wallet"]
        agent_id = data["agent"]
        agent_id = int(agent_id)
        agent = Agent.objects.get(id=agent_id)
        new_data = agent.profile.email
        qty = data["qty"]
        qty = int(qty)
        product = data["product"]
        home_del = data["home_del"]
        unit_price = data["unit_price"]
        unit_price = int(unit_price)
        tkn = request.META.get('HTTP_AUTHORIZATION', '').split(' ', 1)[1]
        us = Token.objects.get(key=tkn).user
        bl = Wallet.objects.get(user=us)
        # agent notification settings
        agent_email = agent.profile.email
        agent_name = agent.profile.username
        customer_name = us.username
        phone_number = us.phone_number
        if wallet == "1, Shop balance, true, null":
            if total <= bl.shop:
                delivery_type = "Paid from Wallet(shop balance)"
                order = Order.objects.create(user=us,total=total,wallet="shop",
                                                agent=agent,
                                                qty=qty,product=product,
                                                home_del=home_del,
                                                unit_price=unit_price,
                                                status = "pending",
                                            )
                order.save()
                bl.shop -= total
                bl.save()
                send_mail(
                    "Product Delivery alert",
                    f"Dear Agent {agent_name}\nyou have got a new order.here is your order details\n\ncustomer name : {customer_name}\nProduct Name: {product}\nCustomer Phone Number: {phone_number}\nDelivery Type: Paid from shop balance\nTotal ammount: {total}",
                    'azabazar@azabazar.com',
                    [agent_email ],
                    fail_silently=False
                    )
                return Response(status=status.HTTP_200_OK)
        elif wallet == "2, Cash balance, true, null":
            if total <= bl.cash:
                delivery_type = "Paid from Wallet(cash balance)"
                order = Order.objects.create(user=us,total=total,wallet="cash balance",
                                                agent=agent,
                                                qty=qty,product=product,
                                                home_del=home_del,
                                                unit_price=unit_price,
                                                status = "pending",
                                            )
                order.save()
                bl.cash -= total
                bl.save()
                send_mail(
                    "Product Delivery alert",
                    f"Dear Agent {agent_name}\nyou have got a new order.here is your order details\n\ncustomer name : {customer_name}\nProduct Name: {product}\nCustomer Phone Number: {phone_number}\nDelivery Type: Paid from cash balance\nTotal ammount: {total}",
                    'azabazar@azabazar.com',
                    [agent_email ],
                    fail_silently=False
                    )
                return Response(status=status.HTTP_200_OK)
        elif wallet == "0, Cash on delivery, true, null":
            delivery_type = "Cash on delivery"
            order = Order.objects.create(user=us,total=total,wallet="cash",
                                            agent=agent,
                                            qty=qty,product=product,
                                            home_del=home_del,
                                            unit_price=unit_price,
                                            status = "pending",
                                        )
            order.save()
            send_mail(
                "Product Delivery alert",
                f"Dear Agent {agent_name}\nyou have got a new order.here is your order details\n\ncustomer name : {customer_name}\nProduct Name: {product}\nCustomer Phone Number: {phone_number}\nDelivery Type: Cash on delivery\nTotal ammount: {total}",
                'azabazar@azabazar.com',
                [agent_email ],
                fail_silently=False
                )
            return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)
@api_view(['POST'], )
def orderHomeAPI(request):
    if request.method == 'POST':
        data = request.data
        total = data['total']
        total = float(total)
        qty = data["qty"]
        qty = int(qty)
        unit_price = data["unit_price"]
        unit_price = int(unit_price)
        product = data["product"]
        home_del = data["home_del"]
        address = data["address"]
        wallet = data["wallet"]
        tkn = request.META.get('HTTP_AUTHORIZATION', '').split(' ', 1)[1]
        us = Token.objects.get(key=tkn).user
        bl = Wallet.objects.get(user=us)
        if wallet == "1, Shop balance, true, null":
            if total <= bl.shop:
                order = Order.objects.create(
                                                user=us,total=total,wallet="shop wallet",
                                                qty=qty,product=product,
                                                home_del=home_del,
                                                unit_price=unit_price,
                                                address = address,
                                                status = "pending",
                                            )
                order.save()
                bl.shop -= total
                bl.save()
                return Response(status=status.HTTP_200_OK)
        elif wallet == "0, Cash on delivery, true, null":
            order = Order.objects.create(
                                            user=us,total=total,wallet="cash on delivery",
                                            qty=qty,product=product,
                                            home_del=home_del,
                                            unit_price=unit_price,
                                            address = address,
                                            status = "pending",
                                        )
            order.save()
            return Response(status=status.HTTP_200_OK)
        elif wallet == "2, Cash balance, true, null":
            if total <= bl.cash:
                delivery_type = "Paid from Wallet(cash balance)"
                order = Order.objects.create(user=us,total=total,wallet="cash balance",
                                                qty=qty,product=product,
                                                home_del=home_del,
                                                unit_price=unit_price,
                                                address = address,
                                                status = "pending",
                                            )
                order.save()
                bl.cash -= total
                bl.save()
                return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
class OrderView(APIView):
    def get(self, request, format=None):
        tkn = request.META.get('HTTP_AUTHORIZATION', '').split(' ', 1)[1]
        us = Token.objects.get(key=tkn).user
        order = Order.objects.filter(user=us, status='pending')
        serializer = OrderSerializer(order, many=True)
        return Response(serializer.data)
@api_view(['POST'], )
def incometoshop(request):
    if request.method == "POST":
        data = request.data
        ammount = data["ammount"]
        ammount = int(ammount)
        pswd = data["password"]
        tkn = request.META.get('HTTP_AUTHORIZATION', '').split(' ', 1)[1]
        us = Token.objects.get(key=tkn).user
        acc = Account.objects.get(username=us.username)
        blnc = Wallet.objects.get(user=us)
        if check_password(pswd, acc.password):
            if ammount <= blnc.income:
                blnc.income -= ammount
                blnc.shop += ammount - ammount*0.10
                blnc.save()
                data = {
                    "success": "transfered to shop wallet"
                }
                return Response(data)
    data = {
        "error": "was not transfered"
    }
    return Response(data)

@api_view(['POST'], )
def shoptoshop(request):
    if request.method == "POST":
        data = request.data
        ammount = data["ammount"]
        ammount = int(ammount)
        pswd = data["password"]
        receiver_nmbr = data["number"]
        tkn = request.META.get('HTTP_AUTHORIZATION', '').split(' ', 1)[1]
        us = Token.objects.get(key=tkn).user
        acc = Account.objects.get(username=us.username)
        # rcvr_account = Account.objects.get(phone_number=receiver_nmbr)
        blnc = Wallet.objects.get(user=us)
        rcvr = Wallet.objects.get(user__phone_number=receiver_nmbr)
        if check_password(pswd, acc.password):
            if ammount <= blnc.shop:
                blnc.shop -= ammount
                rcvr.shop += ammount
                blnc.save()
                rcvr.save()
                data = {
                    "success": "transfered to another wallet"
                }
                return Response(data)
    data = {
        "error": "was not transfered"
    }
    return Response(data)
@api_view(['POST'], )
def cashtocash(request):
    data = request.data
    ammount = data["ammount"]
    ammount = int(ammount)
    pswd = str(data["password"])
    receiver_nmbr = str(data["number"])
    # receiver_nmbr = int(receiver_nmbr)
    tkn = request.META.get('HTTP_AUTHORIZATION', '').split(' ', 1)[1]
    us = Token.objects.get(key=tkn).user
    acc = Account.objects.get(username=us.username)
    # rcvr_account = Account.objects.get(username='evan1337')
    blnc = Wallet.objects.get(user=us)
    rcvr = Wallet.objects.get(user__phone_number=receiver_nmbr)
    if check_password(pswd, acc.password):
        if ammount <= blnc.cash:
            blnc.cash -= ammount
            rcvr.cash += ammount
            blnc.save()
            rcvr.save()
            data = {
                "success": "transfered to another wallet"
            }
            return Response(data, status=status.HTTP_200_OK)
    data = {
        "error": "was not transfered"
    }
    return Response(data, status=status.HTTP_404_BAD_REQUEST)
class WalletView(APIView):
    def get(self, request, format=None):
        tkn = request.META.get('HTTP_AUTHORIZATION', '').split(' ', 1)[1]
        us = Token.objects.get(key=tkn).user
        wallet = Wallet.objects.get(user=us)
        serializer = WalletSerializer(wallet)
        return Response(serializer.data)

@api_view(["GET"],)
def order_received(request, id=None):
    id = id
    tkn = request.META.get('HTTP_AUTHORIZATION', '').split(' ', 1)[1]
    us = Token.objects.get(key=tkn).user
    orders = Order.objects.filter(id=id, user=us)
    pd_name = Order.objects.filter(id=id, user=us).first().product
    if Products.objects.filter(title=pd_name, unit_point__isnull=True).exists():
        orders.update(status="received")
        data = {"received": "order received"}
        return Response(data)
    else:
        unit_point = Products.objects.filter(title=pd_name).first().unit_point
        ow = Wallet.objects.get(user=us)
        owr = us.refer
        gone= Account.objects.filter(phone_number=owr).first()
        gone_owr = Wallet.objects.get(user=gone)
        gone_owr.income += unit_point
        ow.income += unit_point
        ow.save()
        gone_owr.save()
        orders.update(status="received")
        data = {"received": "order received"}
        return Response(data)
    return Response(data)
class OrderReceivedView(APIView):
    def get(self, request, format=None):
        tkn = request.META.get('HTTP_AUTHORIZATION', '').split(' ', 1)[1]
        us = Token.objects.get(key=tkn).user
        order = Order.objects.filter(user=us, status='received').order_by('-id')
        serializer = OrderSerializer(order, many=True)
        return Response(serializer.data)