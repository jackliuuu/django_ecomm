import datetime
import pytz
from django.core.mail import EmailMultiAlternatives
from django.db import connection
from django.template.loader import render_to_string
from django.utils.translation import get_language

from products.models import Product
from .models import EPaperEmail
from core.models import Setting
from customers.models import Client


def task_epaper_send_email(schema):
    connection.set_schema(schema)
    client = Client.objects.get(schema_name=schema)
    domain = client.domains.all().first().domain
    tz = pytz.timezone('Asia/Taipei')
    today = tz.localize(datetime.datetime.now())
    new_products = Product.objects.filter(created__gte=today)
    language = get_language()
    setting = Setting.objects.get(id = language)
    context = {
        'host' : f'http://{domain}:8000',
        'sitename': setting.sitename,
        'products': new_products
    }
    bcc = EPaperEmail.objects.all()
    subject = '新品快訊'
    text_context = render_to_string('epaper/new_products_email.txt',context)
    html_context = render_to_string('epaper/new_products_email.html',context)
    msg = EmailMultiAlternatives(subject,text_context,None,to=[],bcc=bcc)
    msg.attach_alternative(html_context,"text/html")
    msg.send()
    return {'status':'OK'}
    