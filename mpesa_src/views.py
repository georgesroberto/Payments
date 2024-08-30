import json
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django_daraja.mpesa.core import MpesaClient
from .models import MpesaTransaction
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def index(request):
    return render(request, 'index.html')


def initiate_stk_payment(request):
    cl = MpesaClient()
    phone_number = '254796807438'
    amount = 1
    account_reference = 'reference'
    transaction_desc = 'Description'
    callback_url = 'https://07b3-197-232-118-208.ngrok-free.app/callback'
    
    response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)

    MpesaTransaction.objects.create(
        merchant_request_id=response.merchant_request_id,
        checkout_request_id=response.checkout_request_id,
        amount=amount,
        phone_number=phone_number,
        status='pending'
    )

    return render(request, 'payment_processing.html')


def check_payment_status(request):
    # This logic is just an example; you should tailor it to your actual status check
    transaction = MpesaTransaction.objects.filter(phone_number='254796807438').last()
    print(transaction.status)
    
    if transaction and transaction.status == 'Success':
        return JsonResponse({'status': 'paid'})
    elif transaction and transaction.status == 'Failed':
        return JsonResponse({'status': 'failed'})
    else:
        return JsonResponse({'status': 'pending'})


import json
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import MpesaTransaction

logger = logging.getLogger(__name__)

@csrf_exempt
def callback(request):
    logger.info(f"Callback reached with method: {request.method}")

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            transaction_status = data.get('Body', {}).get('stkCallback', {}).get('ResultCode')
            checkout_request_id = data.get('Body', {}).get('stkCallback', {}).get('CheckoutRequestID')

            transaction = MpesaTransaction.objects.get(checkout_request_id=checkout_request_id)
            logger.info(f"Transaction retrieved: {transaction}")
            
            if transaction_status == 0:
                transaction.status = 'paid'
                transaction.save()
                logger.info(f"Transaction successful: {transaction}")
                return JsonResponse({'status': 'Success'}, status=200)
            else:
                transaction.status = 'failed'
                transaction.save()
                logger.info(f"Transaction failed: {transaction}")
                return JsonResponse({'status': 'Failed'}, status=200)
        except Exception as e:
            logger.error(f"Error processing callback: {e}")
    
    logger.info(f"Callback finished with method: {request.method}")
    return JsonResponse({'status': 'Invalid request'}, status=400)


def paid_view(request):
    return HttpResponse("Payment made successfully")


def error_view(request):
    return HttpResponse("Payment failed")
