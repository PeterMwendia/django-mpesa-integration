from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from django_daraja.mpesa.core import MpesaClient
from fastapi import Request, Path
from fastapi import FastAPI

from .forms import LoginForm, RegistrationForm

from django.contrib.auth import login, authenticate, logout

mpesa = FastAPI()
from .callback_db import create_table, populate_table
from .models import Transaction, CustomUser
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    cl = MpesaClient()
    # Use a Safaricom phone number that you have access to, for you to be able to view the prompt.
    phone_number = '+254743105374'
    amount = 1
    account_reference = 'Token Purchase'
    transaction_desc = 'Description'
    # callback_url = 'https://darajambili.herokuapp.com/express-payment';
    callback_url = 'https://api.darajambili.com/express-payment'
    response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
    # return HttpResponse(response)
    response_json = response.json()
    return JsonResponse(response_json)
    
@login_required
def stk_push_callback(request):
        data = request.body
        
        return HttpResponse(data)
        # return HttpResponse("STK Push in Django👋")
        
@login_required
@mpesa.post("/callbackdata")
async def callback(request: Request):
    json_data = await request.json()
    transactions = []
    merchant_request_id = json_data['Body']['stkCallback']['MerchantRequestID']
    checkout_request_id = json_data['Body']['stkCallback']['CheckoutRequestID']
    result_code = json_data['Body']['stkCallback']['ResultCode']
    result_desc = json_data['Body']['stkCallback']['ResultDesc']
    amount = json_data['Body']['stkCallback']['CallbackMetadata']['Item'][0]['Value']
    mpesa_receipt_number = json_data['Body']['stkCallback']['CallbackMetadata']['Item'][1]['Value']
    transaction_date = json_data['Body']['stkCallback']['CallbackMetadata']['Item'][2]['Value']
    phone_number = json_data['Body']['stkCallback']['CallbackMetadata']['Item'][3]['Value']
    transactions.append((merchant_request_id, checkout_request_id, result_code, result_desc, amount, mpesa_receipt_number, transaction_date, phone_number))

    create_table("Mpesa", ["merchant_request_id VARCHAR(255)","checkout_request_id VARCHAR(255)","result_code INTEGER","result_desc VARCHAR(255)","amount INTEGER","mpesa_receipt_number VARCHAR(255)","transaction_date VARCHAR(255)","phone_number VARCHAR(255)"])
    populate_table("Mpesa", transactions)
    
def express_payment_callback(request):
    
    return HttpResponse("")


@login_required
def transaction_list(request):
    transactions = Transaction.objects.all()
    return render(request, 'mpesa/transactions.html', {'transactions': transactions})


@login_required
def view_all_users(request):
    users = CustomUser.objects.all()
    return render(request, 'mpesa/users.html', {'users': users})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            login(request, user)
            return redirect('login')  # Redirect to the desired URL after successful registration
    else:
        form = RegistrationForm()
    return render(request, 'mpesa/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')  # Redirect to the desired URL after successful login
    else:
        form = LoginForm()
    return render(request, 'mpesa/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')  # Redirect to the desired URL after logout