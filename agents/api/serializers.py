from rest_framework import serializers
from agents.models import Order, Wallet

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('user', 'wallet', 'agent', 'home_del', 'product', 'qty', 'total', 'id', 'unit_price')
class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ('shop', 'income', 'cash')