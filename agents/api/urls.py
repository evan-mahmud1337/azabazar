from django.urls import path
from . import views

urlpatterns = [
    path('order/', views.orderAPI, name="order"),
    path('orderhome/', views.orderHomeAPI, name="orderhome"),
    path('incometoshop/', views.incometoshop, name="incometoshop"),
    path('cashtocash/', views.cashtocash, name="cashtocash"),
    path('shoptoshop/', views.shoptoshop, name="shoptoshop"),
    path('orderlist/', views.OrderView.as_view(), name="orderlist"),
    path('order_received_list/', views.OrderReceivedView.as_view(), name="orderreceivedlist"),
    path('wallet/', views.WalletView.as_view()),
    path('order_receive/<id>/', views.order_received, name='order_receive'),
]