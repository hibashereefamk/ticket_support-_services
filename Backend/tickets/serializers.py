from rest_framework import serializers
from .models import Ticket

class TicketSeriliazer(serializers.ModelSerializer):
    class meta:
        model =Ticket
        fields ='__all__'

        