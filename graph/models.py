from django.db import models

# Create your models here.
class LoraPacket(models.Model):
    value = models.TextField(null=True, blank = True)
    date_received = models.DateTimeField(auto_now_add=True)
    pm25 = models.FloatField(null=True, blank=True)
    temperature = models.FloatField(null=True, blank=True)
    humidity = models.FloatField(null=True, blank=True)
    pressure = models.FloatField(null=True, blank=True)


# signals

import channels.layers

from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync

from .models import LoraPacket


def send_message(event):
    '''
    Send message to the browser
    '''
    print("send_message triggered")
    message = event['text']
    channel_layer = channels.layers.get_channel_layer()
    # Send message to WebSocket
    async_to_sync(channel_layer.send)(text_data=json.dumps(
        message
    ))

@receiver(post_save, sender=LoraPacket, dispatch_uid='update_graph')
def update_graph(sender, instance, **kwargs):
    '''
    Sends latest LoraPacket to browser graph after LoraPacket save
    '''
    group_name = 'dashboard'
    print("update_graph triggered")

    message = {
        'pm25': instance.pm25,
        'date_received': instance.date_received.isoformat(),
        'temperature': instance.temperature,
        'pressure': instance.pressure,
        'humidity': instance.humidity
    }

    channel_layer = channels.layers.get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': 'send_message',
            'text': message
        }
    )
