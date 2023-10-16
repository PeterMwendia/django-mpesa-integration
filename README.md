# django-mpesa-integration
 django mpesa stk-push integration


## Installation

To get started first clone the repo by running:
```bash
    git clone https://github.com/PeterMwendia/django-mpesa-integration.git
    cd django-mpesa-integration
    rm -rf .git
```
To install the packages, run
```bash
    python3 -m venv .venv
    pip install wheel
    pip install -r requirements.txt
```
create .env file with the following variable:-

    # .env file
    DJANGO_SECRET_KEY=
    DJANGO_DEBUG=
    POSTGRES_DB=
    POSTGRES_USER=
    POSTGRES_PASSWORD=
    POSTGRES_HOST=
    POSTGRES_PORT=
    DJANGO_ALLOWED_HOSTS=your_domain.com

To test the app, run
```bash
    python manage.py makemigrations
    python manage.py migrate
    python manage.py collectstatic --no-input
    daphne my_site.asgi:application -b 0.0.0.0 -p 8000
```

Read the full documentation at https://django-daraja.readthedocs.io

MPESA Daraja API documentation can be found at https://developer.safaricom.co.ke

## Examples

### STK Push

An example, to send an STK push prompt to customer phone, then display response message

```python
    from django_daraja.mpesa.core import MpesaClient

    def index(request):
        cl = MpesaClient()
        phone_number = '0700111222'
        amount = 1
        account_reference = 'reference'
        transaction_desc = 'Description'
        callback_url = 'https://api.darajambili.com/express-payment'
        response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
        return HttpResponse(response)
```

On your browser, you will receive a message `Success. Request accepted for processing` on success of the STK push, and on the phone number specified you will receive an MPESA PIN prompt. Once the transaction is complete, you will receive a notification on the callback URL you provided. If you used the exact callback URL in the example above (i.e. https://api.darajambili.com/express-payment), you can head over to https://darajambili.com to view the notification received

### B2C Payment

An example, to perform a BusinessPayment B2C (Business to Customer) transaction

```python
    from django_daraja.mpesa.core import MpesaClient

    def index(request):
        cl = MpesaClient()
        phone_number = '0700111222'
        amount = 1
        transaction_desc = 'Business Payment Description'
        occassion = 'Test business payment occassion'
        callback_url = 'https://api.darajambili.com/b2c/result'
        response = cl.business_payment(phone_number, amount, transaction_desc, callback_url, occassion)
        return HttpResponse(response)

```

On your browser, you will receive a message `Accept the service request successfully.` on success of the transaction. Once the transaction is complete, you will receive a notification on the callback URL you provided. If you used the exact callback URL in the example above (i.e. https://api.darajambili.com/b2c/result), you can head over to https://darajambili.com to view the notification received
