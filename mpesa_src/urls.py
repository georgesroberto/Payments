from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('initiate/', views.initiate_stk_payment, name='initiate_stk_payment'),
    path('callback/', views.callback, name='callback'),
    path('paid/', views.paid_view, name='paid'),
    path('payment_failed/', views.error_view, name='error'),
    path('check_payment_status/', views.check_payment_status, name='check_payment_status'),
]
