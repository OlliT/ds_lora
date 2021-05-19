from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from textwrap import wrap
from .models import *
import json

def index(request):
    return render(request, 'base.html', context={'text': 'Hello World'})

@csrf_exempt
def lora(request):
    if request.method == 'POST':
        print('Raw Data: "%s"' % request.body)
        body = json.loads(request.body)
        if 'DevEUI_notification' in body:
            return HttpResponse("OK")
        if not 'DevEUI_uplink' in body:
            return HttpResponse("Not a valid lora package")
        message = body['DevEUI_uplink']
        payload = message['payload_hex']
        print('Payload: "%s"' % payload)

        #create a list of 4 digit hex values
        l = wrap(payload,4)

        #[temp*100, pres/2, hum*100, pm1, pm25, pm10]
        temp = int(l[0],16) / 100
        pres = int(l[1],16) * 2
        hum = int(l[2],16) / 100
        pm1 = int(l[3],16)
        pm25 = int(l[4],16)
        pm10 = int(l[5],16)
        print(f'PM25: {pm25}')
        print(f'temp: {temp}')
        print(f'humidity: {hum}')
        print(f'pressure: {pres}')

        p = LoraPacket(
            value=payload, pm25 = pm25, temperature = temp,
            humidity=hum, pressure = pres
        )
        p.save()
    else:
        print('request.method is not POST')
    return HttpResponse("OK")