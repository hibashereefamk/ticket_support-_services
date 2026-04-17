# tickets/tasks.py

from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Ticket
from .utils import classify_ticket
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


@shared_task
def test_task():
    print("Celery is working!")


@shared_task
def process_ticket_task(ticket_id):
    try:
        ticket = Ticket.objects.get(id=ticket_id)

        # classify ticket
        result = classify_ticket(ticket.description)

        ticket.category = result["category"]
        ticket.priority = result["priority"]
        ticket.save()

        print(f"Ticket {ticket_id} processed successfully")

        # ✅ SEND WEBSOCKET NOTIFICATION HERE
        channel_layer = get_channel_layer()

        async_to_sync(channel_layer.group_send)(
            "notifications",   # must match consumer group
            {
                "type": "send_notification",
                "message": f"Ticket {ticket.id} processed!"
            }
        )

    except Ticket.DoesNotExist:
        print(f"Ticket {ticket_id} not found")

@shared_task
def send_ticket_confirmation_email(ticket_id):
    try:
        ticket = Ticket.objects.get(id=ticket_id)

        subject = "Ticket Created Successfully"
        message = f"Your ticket has been created with ID: {ticket.id}"
        recipient_list = [ticket.user.email]

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            recipient_list,
            fail_silently=False,
        )

        print(f"Email sent for Ticket {ticket_id}")

    except Ticket.DoesNotExist:
        print(f"Ticket {ticket_id} not found")
@shared_task
def process_all_tickets():
    tickets = Ticket.objects.filter(status='open')  # or remove filter if not needed

    for ticket in tickets:
        result = classify_ticket(ticket.description)

        ticket.category = result["category"]
        ticket.priority = result["priority"]
        ticket.save()

    print("All tickets processed by Celery Beat")